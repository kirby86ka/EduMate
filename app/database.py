import firebase_admin
from firebase_admin import credentials, firestore
from typing import Optional, Dict, List, Any
import logging
from app.config import settings
import os

logger = logging.getLogger(__name__)


class FirestoreCollection:
    """Wrapper class for Firestore collection operations with MongoDB-like API"""
    
    def __init__(self, collection_ref):
        self.collection_ref = collection_ref
    
    async def insert_one(self, document: Dict[str, Any]):
        """Insert a single document"""
        if "_id" in document:
            doc_id = str(document["_id"])
            del document["_id"]
            doc_ref = self.collection_ref.document(doc_id)
            doc_ref.set(document)
            return type('InsertResult', (), {'inserted_id': doc_id})()
        else:
            update_time, doc_ref = self.collection_ref.add(document)
            return type('InsertResult', (), {'inserted_id': doc_ref.id})()
    
    async def insert_many(self, documents: List[Dict[str, Any]]):
        """Insert multiple documents"""
        inserted_ids = []
        for doc in documents:
            result = await self.insert_one(doc.copy())
            inserted_ids.append(result.inserted_id)
        return type('InsertManyResult', (), {'inserted_ids': inserted_ids})()
    
    async def find_one(self, filter_dict: Dict[str, Any]):
        """Find a single document matching filter"""
        if not filter_dict:
            docs = self.collection_ref.limit(1).stream()
            for doc in docs:
                return {"_id": doc.id, **doc.to_dict()}
            return None
        
        if "_id" in filter_dict:
            doc = self.collection_ref.document(str(filter_dict["_id"])).get()
            if doc.exists:
                return {"_id": doc.id, **doc.to_dict()}
            return None
        
        query = self.collection_ref
        for key, value in filter_dict.items():
            query = query.where(key, '==', value)
        
        docs = query.limit(1).stream()
        for doc in docs:
            return {"_id": doc.id, **doc.to_dict()}
        return None
    
    def find(self, filter_dict: Optional[Dict[str, Any]] = None):
        """Find documents matching filter"""
        return FirestoreCursor(self.collection_ref, filter_dict or {})
    
    async def update_one(self, filter_dict: Dict[str, Any], update: Dict[str, Any]):
        """Update a single document"""
        doc_data = await self.find_one(filter_dict)
        if not doc_data:
            return type('UpdateResult', (), {'modified_count': 0})()
        
        doc_id = doc_data["_id"]
        doc_ref = self.collection_ref.document(doc_id)
        
        update_data = {}
        if "$set" in update:
            update_data.update(update["$set"])
        
        if "$inc" in update:
            current_data = doc_ref.get().to_dict() or {}
            for key, value in update["$inc"].items():
                update_data[key] = current_data.get(key, 0) + value
        
        if update_data:
            doc_ref.update(update_data)
            return type('UpdateResult', (), {'modified_count': 1})()
        return type('UpdateResult', (), {'modified_count': 0})()
    
    async def delete_many(self, filter_dict: Dict[str, Any]):
        """Delete documents matching filter"""
        docs = await self.find(filter_dict).to_list(length=None)
        deleted_count = 0
        for doc in docs:
            self.collection_ref.document(doc["_id"]).delete()
            deleted_count += 1
        return type('DeleteResult', (), {'deleted_count': deleted_count})()
    
    async def count_documents(self, filter_dict: Dict[str, Any]):
        """Count documents matching filter"""
        docs = await self.find(filter_dict).to_list(length=None)
        return len(docs)


class FirestoreCursor:
    """Cursor for Firestore query results with MongoDB-like API"""
    
    def __init__(self, collection_ref, filter_dict: Dict[str, Any]):
        self.collection_ref = collection_ref
        self.filter_dict = filter_dict
        self.sort_field = None
        self.sort_direction = 'ASCENDING'
    
    async def to_list(self, length: Optional[int] = None):
        """Convert cursor to list of documents"""
        query = self.collection_ref
        
        for key, value in self.filter_dict.items():
            if key != "_id":
                query = query.where(key, '==', value)
        
        if self.sort_field:
            query = query.order_by(
                self.sort_field, 
                direction=firestore.Query.DESCENDING if self.sort_direction == 'DESCENDING' else firestore.Query.ASCENDING
            )
        
        if length:
            query = query.limit(length)
        
        docs = query.stream()
        result = []
        for doc in docs:
            result.append({"_id": doc.id, **doc.to_dict()})
        
        if "_id" in self.filter_dict:
            result = [d for d in result if d["_id"] == str(self.filter_dict["_id"])]
        
        return result
    
    def sort(self, key: str, direction: int = 1):
        """Sort results by field"""
        self.sort_field = key
        self.sort_direction = 'DESCENDING' if direction == -1 else 'ASCENDING'
        return self


class DatabaseManager:
    def __init__(self):
        self.db = None
        self.firebase_app = None
        
    async def connect(self):
        """Initialize Firebase connection"""
        try:
            firebase_creds_path = settings.firebase_credentials_path
            
            if firebase_creds_path and os.path.exists(firebase_creds_path):
                if not firebase_admin._apps:
                    cred = credentials.Certificate(firebase_creds_path)
                    self.firebase_app = firebase_admin.initialize_app(cred)
                
                self.db = firestore.client()
                logger.info("Successfully connected to Firebase Firestore")
            else:
                logger.error(f"Firebase credentials not found at: {firebase_creds_path}")
                logger.error("Please follow the instructions in FIREBASE_SETUP.md to configure Firebase")
                raise Exception(
                    f"Firebase credentials not configured. "
                    f"Expected credentials file at: {firebase_creds_path}. "
                    f"See FIREBASE_SETUP.md for setup instructions."
                )
                
        except Exception as e:
            if "Firebase credentials not configured" in str(e):
                raise
            logger.error(f"Failed to initialize Firebase: {e}")
            raise Exception(f"Firebase initialization failed: {e}")
    
    async def close(self):
        """Close Firebase connection"""
        if self.firebase_app:
            firebase_admin.delete_app(self.firebase_app)
            logger.info("Firebase connection closed")
    
    def get_collection(self, name: str):
        """Get a Firestore collection"""
        if self.db is None:
            raise Exception("Database not initialized. Call connect() first.")
        return FirestoreCollection(self.db.collection(name))
    
    def is_using_memory(self) -> bool:
        """Check if using in-memory database (always False for Firebase)"""
        return False


db_manager = DatabaseManager()

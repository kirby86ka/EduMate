from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, Dict, List, Any
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class InMemoryDatabase:
    def __init__(self):
        self.collections: Dict[str, List[Dict[str, Any]]] = {
            "questions": [],
            "sessions": [],
            "attempts": [],
            "user_skills": []
        }
        self.id_counters: Dict[str, int] = {
            "questions": 1,
            "sessions": 1,
            "attempts": 1,
            "user_skills": 1
        }
    
    def get_collection(self, name: str):
        if name not in self.collections:
            self.collections[name] = []
            self.id_counters[name] = 1
        return InMemoryCollection(name, self.collections, self.id_counters)


class InMemoryCollection:
    def __init__(self, name: str, collections: Dict, id_counters: Dict):
        self.name = name
        self.collections = collections
        self.id_counters = id_counters
    
    async def insert_one(self, document: Dict[str, Any]):
        if "_id" not in document:
            document["_id"] = str(self.id_counters[self.name])
            self.id_counters[self.name] += 1
        self.collections[self.name].append(document.copy())
        return type('InsertResult', (), {'inserted_id': document["_id"]})()
    
    async def insert_many(self, documents: List[Dict[str, Any]]):
        inserted_ids = []
        for doc in documents:
            if "_id" not in doc:
                doc["_id"] = str(self.id_counters[self.name])
                self.id_counters[self.name] += 1
            self.collections[self.name].append(doc.copy())
            inserted_ids.append(doc["_id"])
        return type('InsertManyResult', (), {'inserted_ids': inserted_ids})()
    
    async def find_one(self, filter_dict: Dict[str, Any]):
        for doc in self.collections[self.name]:
            if self._match_filter(doc, filter_dict):
                return doc.copy()
        return None
    
    def find(self, filter_dict: Optional[Dict[str, Any]] = None):
        filter_dict = filter_dict or {}
        return InMemoryCursor(self.collections[self.name], filter_dict)
    
    async def update_one(self, filter_dict: Dict[str, Any], update: Dict[str, Any]):
        for i, doc in enumerate(self.collections[self.name]):
            if self._match_filter(doc, filter_dict):
                if "$set" in update:
                    doc.update(update["$set"])
                if "$inc" in update:
                    for key, value in update["$inc"].items():
                        doc[key] = doc.get(key, 0) + value
                return type('UpdateResult', (), {'modified_count': 1})()
        return type('UpdateResult', (), {'modified_count': 0})()
    
    async def delete_many(self, filter_dict: Dict[str, Any]):
        original_count = len(self.collections[self.name])
        self.collections[self.name] = [
            doc for doc in self.collections[self.name]
            if not self._match_filter(doc, filter_dict)
        ]
        deleted_count = original_count - len(self.collections[self.name])
        return type('DeleteResult', (), {'deleted_count': deleted_count})()
    
    async def count_documents(self, filter_dict: Dict[str, Any]):
        count = sum(1 for doc in self.collections[self.name] if self._match_filter(doc, filter_dict))
        return count
    
    def _match_filter(self, doc: Dict[str, Any], filter_dict: Dict[str, Any]) -> bool:
        if not filter_dict:
            return True
        for key, value in filter_dict.items():
            if key not in doc or doc[key] != value:
                return False
        return True


class InMemoryCursor:
    def __init__(self, data: List[Dict[str, Any]], filter_dict: Dict[str, Any]):
        self.data = [doc.copy() for doc in data if self._match_filter(doc, filter_dict)]
        self.index = 0
    
    def _match_filter(self, doc: Dict[str, Any], filter_dict: Dict[str, Any]) -> bool:
        if not filter_dict:
            return True
        for key, value in filter_dict.items():
            if key not in doc or doc[key] != value:
                return False
        return True
    
    async def to_list(self, length: Optional[int] = None):
        if length is None:
            return self.data
        return self.data[:length]
    
    def sort(self, key: str, direction: int = 1):
        reverse = direction == -1
        self.data.sort(key=lambda x: x.get(key, ""), reverse=reverse)
        return self


class DatabaseManager:
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None
        self.in_memory_db = InMemoryDatabase()
        self.use_in_memory = settings.use_in_memory
        
    async def connect(self):
        if settings.mongodb_url and not self.use_in_memory:
            try:
                self.client = AsyncIOMotorClient(settings.mongodb_url)
                await self.client.admin.command('ping')
                self.db = self.client[settings.mongodb_db_name]
                self.use_in_memory = False
                logger.info("Successfully connected to MongoDB")
            except Exception as e:
                logger.warning(f"Failed to connect to MongoDB: {e}. Using in-memory storage.")
                self.use_in_memory = True
        else:
            logger.info("Using in-memory storage")
            self.use_in_memory = True
    
    async def close(self):
        if self.client:
            self.client.close()
    
    def get_collection(self, name: str):
        if self.use_in_memory:
            return self.in_memory_db.get_collection(name)
        if self.db is not None:
            return self.db[name]
        return self.in_memory_db.get_collection(name)
    
    def is_using_memory(self) -> bool:
        return self.use_in_memory


db_manager = DatabaseManager()

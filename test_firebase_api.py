#!/usr/bin/env python3
"""Test script to verify Firebase add() return type"""

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    import os
    
    firebase_creds_path = "firebase-credentials.json"
    
    if not os.path.exists(firebase_creds_path):
        print(f"❌ Firebase credentials not found at: {firebase_creds_path}")
        print("This test requires Firebase credentials to verify the API")
        print("See FIREBASE_SETUP.md for instructions")
        exit(1)
    
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_creds_path)
        firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    collection_ref = db.collection('__test_collection__')
    
    print("Testing collection.add() return type...")
    
    result = collection_ref.add({'test': 'data', 'timestamp': firestore.SERVER_TIMESTAMP})
    
    print(f"\nResult type: {type(result)}")
    print(f"Result: {result}")
    
    if isinstance(result, tuple):
        print(f"\nTuple length: {len(result)}")
        print(f"Element 0 type: {type(result[0])}")
        print(f"Element 0: {result[0]}")
        print(f"Element 1 type: {type(result[1])}")
        print(f"Element 1: {result[1]}")
        
        # Try to access id from both elements
        try:
            print(f"\nElement 0 has .id: {hasattr(result[0], 'id')}")
            if hasattr(result[0], 'id'):
                print(f"Element 0.id: {result[0].id}")
        except:
            pass
            
        try:
            print(f"Element 1 has .id: {hasattr(result[1], 'id')}")
            if hasattr(result[1], 'id'):
                print(f"Element 1.id: {result[1].id}")
        except:
            pass
    
    # Clean up
    collection_ref.document(result[1].id).delete() if isinstance(result, tuple) else None
    print("\n✅ Test complete")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

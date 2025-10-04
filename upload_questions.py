import asyncio
import json
from app.database import db_manager


async def upload_questions_from_json(json_file_path="questions.json"):
    """
    Upload questions from a JSON file to Firebase Firestore.
    
    Expected JSON format:
    [
        {
            "question": "What is 2 + 2?",
            "option_a": "3",
            "option_b": "4",
            "option_c": "5",
            "option_d": "6",
            "correct_answer": "B",
            "difficulty": "easy",
            "subject": "Maths",
            "topic": "Arithmetic"
        },
        ...
    ]
    """
    await db_manager.connect()
    
    try:
        with open(json_file_path, 'r') as file:
            questions = json.load(file)
        
        if not isinstance(questions, list):
            raise ValueError("JSON file must contain an array of questions")
        
        questions_collection = db_manager.get_collection("questions")
        
        print(f"Uploading {len(questions)} questions to Firebase...")
        
        result = await questions_collection.insert_many(questions)
        
        print(f"✓ Successfully uploaded {len(result.inserted_ids)} questions!")
        print(f"\nBreakdown by subject:")
        
        subjects = {}
        for q in questions:
            subject = q.get('subject', 'Unknown')
            subjects[subject] = subjects.get(subject, 0) + 1
        
        for subject, count in subjects.items():
            print(f"  {subject}: {count} questions")
            
    except FileNotFoundError:
        print(f"Error: File '{json_file_path}' not found")
        print("Please create a questions.json file with your questions")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{json_file_path}'")
    except Exception as e:
        print(f"Error uploading questions: {e}")
    finally:
        await db_manager.close()


async def clear_questions():
    """Clear all existing questions from the database."""
    await db_manager.connect()
    
    try:
        questions_collection = db_manager.get_collection("questions")
        result = await questions_collection.delete_many({})
        print(f"✓ Cleared {result.deleted_count} questions from database")
    except Exception as e:
        print(f"Error clearing questions: {e}")
    finally:
        await db_manager.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "clear":
            print("Clearing all questions from database...")
            asyncio.run(clear_questions())
        else:
            asyncio.run(upload_questions_from_json(sys.argv[1]))
    else:
        asyncio.run(upload_questions_from_json())

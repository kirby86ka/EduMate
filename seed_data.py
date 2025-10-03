import asyncio
from app.database import db_manager
from app.models import Question, DifficultyLevel


async def seed_questions():
    await db_manager.connect()
    
    questions_collection = db_manager.get_collection("questions")
    
    await questions_collection.delete_many({})
    
    python_questions = [
        {
            "question": "What is a list in Python?",
            "option_a": "A mutable ordered sequence",
            "option_b": "An immutable sequence",
            "option_c": "A key-value pair collection",
            "option_d": "A set of unique values",
            "correct_answer": "A",
            "difficulty": DifficultyLevel.EASY,
            "subject": "Python",
            "topic": "Data Structures"
        },
        {
            "question": "Which method is used to add an element to the end of a list?",
            "option_a": "add()",
            "option_b": "append()",
            "option_c": "insert()",
            "option_d": "extend()",
            "correct_answer": "B",
            "difficulty": DifficultyLevel.EASY,
            "subject": "Python",
            "topic": "Data Structures"
        },
        {
            "question": "What is the output of: print(type([]))?",
            "option_a": "<class 'tuple'>",
            "option_b": "<class 'dict'>",
            "option_c": "<class 'list'>",
            "option_d": "<class 'set'>",
            "correct_answer": "C",
            "difficulty": DifficultyLevel.EASY,
            "subject": "Python",
            "topic": "Types and Classes"
        },
        {
            "question": "What does the 'self' parameter represent in a Python class method?",
            "option_a": "The class itself",
            "option_b": "The instance of the class",
            "option_c": "The parent class",
            "option_d": "The method name",
            "correct_answer": "B",
            "difficulty": DifficultyLevel.MEDIUM,
            "subject": "Python",
            "topic": "Object-Oriented Programming"
        },
        {
            "question": "Which decorator is used to create a class method in Python?",
            "option_a": "@staticmethod",
            "option_b": "@classmethod",
            "option_c": "@property",
            "option_d": "@method",
            "correct_answer": "B",
            "difficulty": DifficultyLevel.MEDIUM,
            "subject": "Python",
            "topic": "Object-Oriented Programming"
        },
        {
            "question": "What is list comprehension in Python?",
            "option_a": "A way to document lists",
            "option_b": "A concise way to create lists",
            "option_c": "A method to sort lists",
            "option_d": "A function to filter lists",
            "correct_answer": "B",
            "difficulty": DifficultyLevel.MEDIUM,
            "subject": "Python",
            "topic": "Advanced Features"
        },
        {
            "question": "What is a generator in Python?",
            "option_a": "A function that returns multiple values at once",
            "option_b": "A function that uses yield to return values lazily",
            "option_c": "A class that generates random numbers",
            "option_d": "A module for creating objects",
            "correct_answer": "B",
            "difficulty": DifficultyLevel.HARD,
            "subject": "Python",
            "topic": "Advanced Features"
        },
        {
            "question": "What is the time complexity of searching in a Python dict?",
            "option_a": "O(n)",
            "option_b": "O(log n)",
            "option_c": "O(1) average case",
            "option_d": "O(n²)",
            "correct_answer": "C",
            "difficulty": DifficultyLevel.HARD,
            "subject": "Python",
            "topic": "Performance and Algorithms"
        },
        {
            "question": "What is a metaclass in Python?",
            "option_a": "A class that inherits from multiple classes",
            "option_b": "A class of a class",
            "option_c": "An abstract base class",
            "option_d": "A deprecated feature",
            "correct_answer": "B",
            "difficulty": DifficultyLevel.HARD,
            "subject": "Python",
            "topic": "Advanced OOP"
        },
        {
            "question": "What is the Global Interpreter Lock (GIL) in Python?",
            "option_a": "A security feature",
            "option_b": "A mutex that protects Python objects",
            "option_c": "A compilation flag",
            "option_d": "A debugging tool",
            "correct_answer": "B",
            "difficulty": DifficultyLevel.HARD,
            "subject": "Python",
            "topic": "Concurrency"
        },
        {
            "question": "How do you handle exceptions in Python?",
            "option_a": "Using if-else statements",
            "option_b": "Using try-except blocks",
            "option_c": "Using switch-case statements",
            "option_d": "Using error() function",
            "correct_answer": "B",
            "difficulty": DifficultyLevel.EASY,
            "subject": "Python",
            "topic": "Error Handling"
        },
        {
            "question": "What does the 'with' statement do in Python?",
            "option_a": "Imports modules",
            "option_b": "Creates loops",
            "option_c": "Manages context and resources",
            "option_d": "Defines functions",
            "correct_answer": "C",
            "difficulty": DifficultyLevel.MEDIUM,
            "subject": "Python",
            "topic": "Advanced Features"
        },
        {
            "question": "What is the difference between '==' and 'is' in Python?",
            "option_a": "No difference",
            "option_b": "'==' compares values, 'is' compares identity",
            "option_c": "'==' is faster than 'is'",
            "option_d": "'is' is deprecated",
            "correct_answer": "B",
            "difficulty": DifficultyLevel.MEDIUM,
            "subject": "Python",
            "topic": "Fundamentals"
        },
        {
            "question": "What is a lambda function in Python?",
            "option_a": "A named function",
            "option_b": "An anonymous function",
            "option_c": "A recursive function",
            "option_d": "A class method",
            "correct_answer": "B",
            "difficulty": DifficultyLevel.EASY,
            "subject": "Python",
            "topic": "Functions"
        },
        {
            "question": "How do you create a virtual environment in Python?",
            "option_a": "python -m venv env_name",
            "option_b": "virtualenv create",
            "option_c": "python create-env",
            "option_d": "pip install environment",
            "correct_answer": "A",
            "difficulty": DifficultyLevel.EASY,
            "subject": "Python",
            "topic": "Environment Management"
        },
        {
            "question": "What is the purpose of __init__.py?",
            "option_a": "To initialize variables",
            "option_b": "To mark a directory as a Python package",
            "option_c": "To start the application",
            "option_d": "To configure settings",
            "correct_answer": "B",
            "difficulty": DifficultyLevel.MEDIUM,
            "subject": "Python",
            "topic": "Modules and Packages"
        },
        {
            "question": "What does the 'async' keyword do in Python?",
            "option_a": "Makes code run faster",
            "option_b": "Defines an asynchronous function",
            "option_c": "Imports async module",
            "option_d": "Creates threads",
            "correct_answer": "B",
            "difficulty": DifficultyLevel.HARD,
            "subject": "Python",
            "topic": "Asynchronous Programming"
        },
        {
            "question": "What is the difference between shallow and deep copy?",
            "option_a": "Shallow copies nested objects, deep doesn't",
            "option_b": "Deep copies nested objects, shallow doesn't",
            "option_c": "No difference",
            "option_d": "Deep copy is faster",
            "correct_answer": "B",
            "difficulty": DifficultyLevel.MEDIUM,
            "subject": "Python",
            "topic": "Data Structures"
        },
        {
            "question": "What is the purpose of *args and **kwargs?",
            "option_a": "To create variables",
            "option_b": "To pass variable number of arguments",
            "option_c": "To import modules",
            "option_d": "To define classes",
            "correct_answer": "B",
            "difficulty": DifficultyLevel.MEDIUM,
            "subject": "Python",
            "topic": "Functions"
        },
        {
            "question": "What is a decorator in Python?",
            "option_a": "A design pattern",
            "option_b": "A function that modifies another function",
            "option_c": "A syntax error",
            "option_d": "A type of loop",
            "correct_answer": "B",
            "difficulty": DifficultyLevel.HARD,
            "subject": "Python",
            "topic": "Advanced Features"
        }
    ]
    
    javascript_questions = [
        {
            "question": "What is the DOM in JavaScript?",
            "option_a": "Document Object Model",
            "option_b": "Data Object Manager",
            "option_c": "Dynamic Output Method",
            "option_d": "Document Oriented Markup",
            "correct_answer": "A",
            "difficulty": DifficultyLevel.EASY,
            "subject": "JavaScript",
            "topic": "Web APIs"
        },
        {
            "question": "Which keyword is used to declare a constant in JavaScript?",
            "option_a": "var",
            "option_b": "let",
            "option_c": "const",
            "option_d": "constant",
            "correct_answer": "C",
            "difficulty": DifficultyLevel.EASY,
            "subject": "JavaScript",
            "topic": "Variables"
        },
        {
            "question": "What is a closure in JavaScript?",
            "option_a": "A way to close the browser",
            "option_b": "A function with access to outer scope",
            "option_c": "A syntax error",
            "option_d": "A loop statement",
            "correct_answer": "B",
            "difficulty": DifficultyLevel.HARD,
            "subject": "JavaScript",
            "topic": "Functions"
        },
        {
            "question": "What does 'this' keyword refer to in JavaScript?",
            "option_a": "The global object",
            "option_b": "The current execution context",
            "option_c": "The parent function",
            "option_d": "The window object",
            "correct_answer": "B",
            "difficulty": DifficultyLevel.MEDIUM,
            "subject": "JavaScript",
            "topic": "Context"
        },
        {
            "question": "What is event bubbling?",
            "option_a": "Events moving from child to parent",
            "option_b": "Events moving from parent to child",
            "option_c": "Creating new events",
            "option_d": "Removing events",
            "correct_answer": "A",
            "difficulty": DifficultyLevel.MEDIUM,
            "subject": "JavaScript",
            "topic": "Events"
        }
    ]
    
    data_science_questions = [
        {
            "question": "What is a DataFrame in pandas?",
            "option_a": "A one-dimensional array",
            "option_b": "A two-dimensional labeled data structure",
            "option_c": "A plotting library",
            "option_d": "A database connection",
            "correct_answer": "B",
            "difficulty": DifficultyLevel.EASY,
            "subject": "Data Science",
            "topic": "Pandas"
        },
        {
            "question": "What is the difference between supervised and unsupervised learning?",
            "option_a": "Supervised has labeled data, unsupervised doesn't",
            "option_b": "Unsupervised has labeled data, supervised doesn't",
            "option_c": "No difference",
            "option_d": "Supervised is faster",
            "correct_answer": "A",
            "difficulty": DifficultyLevel.MEDIUM,
            "subject": "Data Science",
            "topic": "Machine Learning"
        },
        {
            "question": "What is overfitting in machine learning?",
            "option_a": "Model performs well on training but poor on test data",
            "option_b": "Model performs poorly on both training and test data",
            "option_c": "Model is too simple",
            "option_d": "Model trains too slowly",
            "correct_answer": "A",
            "difficulty": DifficultyLevel.MEDIUM,
            "subject": "Data Science",
            "topic": "Machine Learning"
        },
        {
            "question": "What is the purpose of cross-validation?",
            "option_a": "To speed up training",
            "option_b": "To assess model performance and prevent overfitting",
            "option_c": "To clean data",
            "option_d": "To visualize results",
            "correct_answer": "B",
            "difficulty": DifficultyLevel.HARD,
            "subject": "Data Science",
            "topic": "Model Evaluation"
        },
        {
            "question": "What is numpy primarily used for?",
            "option_a": "Web development",
            "option_b": "Numerical computing with arrays",
            "option_c": "Database management",
            "option_d": "Text processing",
            "correct_answer": "B",
            "difficulty": DifficultyLevel.EASY,
            "subject": "Data Science",
            "topic": "NumPy"
        }
    ]
    
    all_questions = python_questions + javascript_questions + data_science_questions
    
    result = await questions_collection.insert_many(all_questions)
    
    print(f"Successfully seeded {len(result.inserted_ids)} questions!")
    print(f"Database mode: {'In-memory' if db_manager.is_using_memory() else 'MongoDB'}")
    print(f"\nBreakdown:")
    print(f"  Python: {len(python_questions)} questions")
    print(f"  JavaScript: {len(javascript_questions)} questions")
    print(f"  Data Science: {len(data_science_questions)} questions")
    
    await db_manager.close()


if __name__ == "__main__":
    asyncio.run(seed_questions())

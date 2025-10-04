import json
import logging
import os
from typing import Dict, Any, List
from google import genai
from google.genai import types
from pydantic import BaseModel

# IMPORTANT: KEEP THIS COMMENT
# Follow these instructions when using this blueprint:
# - Note that the newest Gemini model series is "gemini-2.5-flash" or gemini-2.5-pro"
#   - do not change this unless explicitly requested by the user
# - Sometimes the google genai SDK has occasional type errors. You might need to run to validate, at time.  
# The SDK was recently renamed from google-generativeai to google-genai. This file reflects the new name and the new APIs.

logger = logging.getLogger(__name__)

# This API key is from Gemini Developer API Key, not vertex AI API Key
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


class Question(BaseModel):
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    explanation: str


class QuestionGenerator:
    """Generate adaptive questions using Gemini AI based on BKT difficulty levels"""
    
    def __init__(self):
        self.client = client
    
    async def generate_question(
        self, 
        subject: str, 
        topic: str, 
        difficulty: str,
        previous_questions: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a question using Gemini AI based on subject, topic, and difficulty.
        
        Args:
            subject: The subject area (Maths, Science, Python)
            topic: The specific topic within the subject
            difficulty: The difficulty level (easy, medium, hard)
            previous_questions: List of previous questions to avoid duplicates
        
        Returns:
            A dictionary containing the generated question
        """
        try:
            difficulty_descriptions = {
                "easy": "basic, introductory level suitable for beginners",
                "medium": "intermediate level requiring some understanding of concepts",
                "hard": "advanced level requiring deep understanding and problem-solving"
            }
            
            previous_context = ""
            if previous_questions:
                previous_context = f"\n\nAvoid generating questions similar to these:\n" + "\n".join(previous_questions[-3:])
            
            system_prompt = f"""You are an expert educational content creator specializing in {subject}.
Generate a {difficulty_descriptions.get(difficulty, 'medium')} multiple-choice question about {topic} in {subject}.

Requirements:
1. The question should be clear and unambiguous
2. Provide exactly 4 options (A, B, C, D)
3. Only ONE option should be correct
4. Include a brief explanation of why the correct answer is right
5. Make the question appropriate for the {difficulty} difficulty level
6. Ensure the question is educational and tests understanding, not just memorization

Respond with JSON matching this exact format:
{{
    "question": "The question text",
    "option_a": "First option",
    "option_b": "Second option", 
    "option_c": "Third option",
    "option_d": "Fourth option",
    "correct_answer": "A" or "B" or "C" or "D",
    "explanation": "Brief explanation of the correct answer"
}}
{previous_context}"""

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Content(role="user", parts=[types.Part(text=f"Generate a {difficulty} question about {topic} in {subject}.")])
                ],
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    response_mime_type="application/json",
                    response_schema=Question,
                ),
            )
            
            raw_json = response.text
            logger.info(f"Generated question JSON: {raw_json}")
            
            if raw_json:
                data = json.loads(raw_json)
                question_data = {
                    "question": data["question"],
                    "option_a": data["option_a"],
                    "option_b": data["option_b"],
                    "option_c": data["option_c"],
                    "option_d": data["option_d"],
                    "correct_answer": data["correct_answer"].upper(),
                    "difficulty": difficulty,
                    "subject": subject,
                    "topic": topic,
                    "explanation": data.get("explanation", "")
                }
                return question_data
            else:
                raise ValueError("Empty response from Gemini")
                
        except Exception as e:
            logger.error(f"Failed to generate question: {e}")
            raise Exception(f"Failed to generate question with Gemini: {e}")
    
    async def generate_topic_for_subject(self, subject: str, difficulty: str) -> str:
        """
        Generate a relevant topic based on the subject and difficulty level.
        
        Args:
            subject: The subject area (Maths, Science, Python)
            difficulty: The difficulty level (easy, medium, hard)
        
        Returns:
            A topic string
        """
        topic_map = {
            "Maths": {
                "easy": ["Arithmetic", "Basic Addition", "Subtraction", "Multiplication", "Division"],
                "medium": ["Algebra", "Geometry", "Fractions", "Percentages", "Equations"],
                "hard": ["Calculus", "Trigonometry", "Statistics", "Advanced Algebra", "Probability"]
            },
            "Science": {
                "easy": ["Biology Basics", "Chemistry Basics", "Physics Basics", "Human Body", "Plants"],
                "medium": ["Cell Biology", "Chemical Reactions", "Forces and Motion", "Energy", "Ecosystems"],
                "hard": ["Genetics", "Organic Chemistry", "Thermodynamics", "Quantum Physics", "Evolution"]
            },
            "Python": {
                "easy": ["Variables", "Data Types", "Basic Operators", "Print Statements", "Input"],
                "medium": ["Lists", "Loops", "Functions", "Dictionaries", "Conditionals"],
                "hard": ["Object-Oriented Programming", "Decorators", "Generators", "Async/Await", "Design Patterns"]
            }
        }
        
        import random
        topics = topic_map.get(subject, {}).get(difficulty, [f"{subject} General"])
        return random.choice(topics)
    
    async def generate_recommendations(self, prompt: str) -> str:
        """
        Generate personalized learning recommendations using Gemini AI.
        
        Args:
            prompt: The prompt containing performance data and request for recommendations
        
        Returns:
            AI-generated recommendations as text
        """
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Content(role="user", parts=[types.Part(text=prompt)])
                ],
            )
            
            return response.text.strip()
        except Exception as e:
            logger.error(f"Failed to generate recommendations: {e}")
            return "Unable to generate personalized recommendations at this time. Please try again later."


question_generator = QuestionGenerator()

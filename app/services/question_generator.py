import json
import logging
import os
import asyncio
from typing import Dict, Any, List, Optional
from google import genai
from google.genai import types
from google.genai.errors import ClientError
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
        self.max_retries = 3
        self.base_delay = 2  # Base delay in seconds
    
    async def _call_with_retry(self, func, *args, **kwargs):
        """
        Call a function with exponential backoff retry logic for transient errors.
        Performs 1 initial attempt + max_retries retry attempts.
        
        Args:
            func: The function to call
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
        
        Returns:
            The result of the function call
        
        Raises:
            Exception: If all retries are exhausted
        """
        last_exception = None
        total_attempts = self.max_retries + 1  # Initial attempt + retries
        
        for attempt in range(total_attempts):
            try:
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(None, lambda: func(*args, **kwargs))
                return result
            except ClientError as e:
                last_exception = e
                error_message = str(e)
                
                # Check if it's a transient error (503, 429, or network issues)
                is_transient = (
                    '503' in error_message or 
                    '429' in error_message or 
                    'UNAVAILABLE' in error_message or
                    'overloaded' in error_message.lower() or
                    'RESOURCE_EXHAUSTED' in error_message
                )
                
                if not is_transient:
                    # Not a transient error, fail immediately
                    logger.error(f"Non-transient error: {e}")
                    raise
                
                if attempt < total_attempts - 1:
                    # Calculate exponential backoff delay
                    delay = self.base_delay * (2 ** attempt)
                    retry_num = attempt + 1
                    logger.warning(f"Transient error: {error_message}. Retry {retry_num}/{self.max_retries} in {delay}s...")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"All {self.max_retries} retry attempts exhausted")
                    raise Exception(f"Failed after {self.max_retries} retries. Last error: {error_message}")
            except Exception as e:
                # Non-ClientError exceptions (parsing errors, etc.)
                logger.error(f"Non-retryable error: {e}")
                raise
        
        # Should never reach here, but just in case
        if last_exception:
            raise last_exception
        raise Exception("Failed to call Gemini API after retries")
    
    async def generate_question(
        self, 
        subject: str, 
        topic: str, 
        difficulty: str,
        previous_questions: Optional[List[str]] = None
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
1. Question MUST be concise and clear (MAX 2 sentences, ideally 1 sentence)
2. Each option MUST be brief and to the point (MAX 15 words per option)
3. Provide exactly 4 options (A, B, C, D)
4. Only ONE option should be correct
5. Explanation should be 1-2 sentences maximum
6. Make the question appropriate for the {difficulty} difficulty level
7. Use LaTeX notation for math (wrap in $ for inline, $$ for display)
8. Use markdown code blocks for code (```python or ```javascript)
9. Keep it simple - avoid overly complex phrasing

Respond with JSON matching this exact format:
{{
    "question": "The question text (max 2 sentences)",
    "option_a": "First option (max 15 words)",
    "option_b": "Second option (max 15 words)", 
    "option_c": "Third option (max 15 words)",
    "option_d": "Fourth option (max 15 words)",
    "correct_answer": "A" or "B" or "C" or "D",
    "explanation": "Brief 1-2 sentence explanation"
}}
{previous_context}"""

            # Run Gemini API call with retry logic for transient errors
            response = await self._call_with_retry(
                self.client.models.generate_content,
                model="gemini-2.5-flash",
                contents=[
                    types.Content(role="user", parts=[types.Part(text=f"Generate a {difficulty} question about {topic} in {subject}.")])
                ],
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    response_mime_type="application/json",
                    temperature=0.7,
                )
            )
            
            # Debug logging
            logger.info(f"Response object type: {type(response)}")
            logger.info(f"Response has text attr: {hasattr(response, 'text')}")
            
            # Check candidates first for safety filters or blocks
            if hasattr(response, 'candidates') and response.candidates:
                logger.info(f"Response has {len(response.candidates)} candidates")
                for i, candidate in enumerate(response.candidates):
                    logger.info(f"Candidate {i} finish_reason: {getattr(candidate, 'finish_reason', 'N/A')}")
                    if hasattr(candidate, 'safety_ratings'):
                        logger.info(f"Candidate {i} safety_ratings: {candidate.safety_ratings}")
                    if hasattr(candidate, 'content'):
                        logger.info(f"Candidate {i} has content: {bool(candidate.content)}")
            
            # Check prompt_feedback for blocks
            if hasattr(response, 'prompt_feedback'):
                logger.info(f"Prompt feedback: {response.prompt_feedback}")
            
            raw_json = response.text if hasattr(response, 'text') and response.text else None
            
            if not raw_json:
                logger.error(f"Empty or no response.text from Gemini for {subject}/{topic}/{difficulty}")
                
                # Try to extract from candidates directly
                if hasattr(response, 'candidates') and response.candidates:
                    for candidate in response.candidates:
                        if hasattr(candidate, 'content') and candidate.content:
                            if hasattr(candidate.content, 'parts') and candidate.content.parts:
                                for part in candidate.content.parts:
                                    if hasattr(part, 'text') and part.text:
                                        raw_json = part.text
                                        logger.info(f"Extracted text from candidate.content.parts: {raw_json[:100]}...")
                                        break
                        if raw_json:
                            break
                
                if not raw_json:
                    raise ValueError("Empty response from Gemini - response.text is None or empty")
            
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
            response = await self._call_with_retry(
                self.client.models.generate_content,
                model="gemini-2.5-flash",
                contents=[
                    types.Content(role="user", parts=[types.Part(text=prompt)])
                ]
            )
            
            return response.text.strip() if response.text else "Unable to generate recommendations at this time."
        except Exception as e:
            logger.error(f"Failed to generate recommendations: {e}")
            return "Unable to generate personalized recommendations at this time. Please try again later."


question_generator = QuestionGenerator()

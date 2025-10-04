from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum


class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Question(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str  
    difficulty: DifficultyLevel
    subject: str
    topic: Optional[str] = None
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "question": "What is a list in Python?",
                "option_a": "A mutable ordered sequence",
                "option_b": "An immutable sequence",
                "option_c": "A key-value pair",
                "option_d": "A set of unique values",
                "correct_answer": "A",
                "difficulty": "easy",
                "subject": "Python",
                "topic": "Data Structures"
            }
        }


class AnswerSubmission(BaseModel):
    session_id: str
    selected_answer: str  
    time_spent: Optional[int] = None
    topic: Optional[str] = None


class AssessmentSession(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    session_id: str
    user_id: Optional[str] = None  
    subject: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    is_active: bool = True
    total_questions: int = 15
    questions_answered: int = 0
    
    class Config:
        populate_by_name = True


class Attempt(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    session_id: str
    question_id: str
    selected_answer: str
    correct_answer: str
    is_correct: bool
    difficulty: DifficultyLevel
    topic: Optional[str] = None
    time_taken_seconds: Optional[int] = None
    answered_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True


class UserSkill(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    session_id: str
    user_id: Optional[str] = None
    subject: str
    topic: str
    mastery_probability: float = 0.5  
    attempts_count: int = 0
    correct_count: int = 0
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True


class BKTParameters(BaseModel):
    p_init: float = 0.1  
    p_learn: float = 0.3  
    p_slip: float = 0.1  
    p_guess: float = 0.25  


class LearningPathTopic(BaseModel):
    topic: str
    mastery_score: float
    priority: str  
    recommended_difficulty: DifficultyLevel
    questions_to_practice: int


class LearningPath(BaseModel):
    session_id: str
    subject: str
    overall_score: float
    mastery_by_topic: Dict[str, float]
    weak_topics: List[LearningPathTopic]
    strong_topics: List[str]
    recommended_course_outline: List[str]
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class SubjectInfo(BaseModel):
    subject: str
    question_count: int
    topics: List[str]


class NextQuestionRequest(BaseModel):
    session_id: str


class NextQuestionResponse(BaseModel):
    session_id: str
    question_number: int
    total_questions: int
    current_difficulty: DifficultyLevel
    mastery_level: float
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    topic: str
    subject: str


class AssessmentComplete(BaseModel):
    session_id: str
    total_questions: int
    correct_answers: int
    accuracy: float
    final_mastery_level: float
    time_taken: int
    weak_topics: List[str]
    strong_topics: List[str]
    recommended_resources: List[str]

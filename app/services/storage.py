from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid


class InMemoryStorage:
    """In-memory storage for sessions, attempts, and user skills"""
    
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.attempts: Dict[str, List[Dict[str, Any]]] = {}
        self.user_skills: Dict[str, Dict[str, Any]] = {}
        self.question_history: Dict[str, List[str]] = {}
    
    def create_session(self, user_id: str, subject: str) -> str:
        """Create a new assessment session"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "session_id": session_id,
            "user_id": user_id,
            "subject": subject,
            "start_time": datetime.utcnow().isoformat(),
            "end_time": None,
            "total_questions": 0,
            "correct_answers": 0,
            "current_difficulty": "easy",
            "mastery_level": 0.0,
            "status": "active"
        }
        self.attempts[session_id] = []
        self.question_history[session_id] = []
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session by ID"""
        return self.sessions.get(session_id)
    
    def update_session(self, session_id: str, updates: Dict[str, Any]):
        """Update session data"""
        if session_id in self.sessions:
            self.sessions[session_id].update(updates)
    
    def add_attempt(self, session_id: str, attempt: Dict[str, Any]):
        """Add an attempt to a session"""
        if session_id not in self.attempts:
            self.attempts[session_id] = []
        
        attempt_data = {
            "attempt_id": str(uuid.uuid4()),
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat(),
            **attempt
        }
        self.attempts[session_id].append(attempt_data)
        return attempt_data
    
    def get_attempts(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all attempts for a session"""
        return self.attempts.get(session_id, [])
    
    def add_question_to_history(self, session_id: str, question: str):
        """Add question to history to avoid duplicates"""
        if session_id not in self.question_history:
            self.question_history[session_id] = []
        self.question_history[session_id].append(question)
    
    def get_question_history(self, session_id: str) -> List[str]:
        """Get question history for a session"""
        return self.question_history.get(session_id, [])
    
    def update_user_skill(self, user_id: str, subject: str, topic: str, mastery: float):
        """Update user skill mastery level"""
        skill_key = f"{user_id}_{subject}_{topic}"
        self.user_skills[skill_key] = {
            "user_id": user_id,
            "subject": subject,
            "topic": topic,
            "mastery_level": mastery,
            "updated_at": datetime.utcnow().isoformat()
        }
    
    def get_user_skill(self, user_id: str, subject: str, topic: str) -> Optional[Dict[str, Any]]:
        """Get user skill data"""
        skill_key = f"{user_id}_{subject}_{topic}"
        return self.user_skills.get(skill_key)
    
    def get_all_user_skills(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all skills for a user"""
        return [
            skill for key, skill in self.user_skills.items()
            if skill["user_id"] == user_id
        ]
    
    def complete_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Mark session as complete and return final data"""
        if session_id in self.sessions:
            self.sessions[session_id]["status"] = "completed"
            self.sessions[session_id]["end_time"] = datetime.utcnow().isoformat()
            return self.sessions[session_id]
        return None
    
    def get_analytics_data(self) -> Dict[str, Any]:
        """Get analytics data for Power BI integration"""
        total_sessions = len(self.sessions)
        completed_sessions = sum(1 for s in self.sessions.values() if s["status"] == "completed")
        total_attempts = sum(len(attempts) for attempts in self.attempts.values())
        
        correct_attempts = 0
        for attempts_list in self.attempts.values():
            correct_attempts += sum(1 for a in attempts_list if a.get("is_correct", False))
        
        accuracy = (correct_attempts / total_attempts * 100) if total_attempts > 0 else 0
        
        subject_performance = {}
        for session in self.sessions.values():
            subject = session["subject"]
            if subject not in subject_performance:
                subject_performance[subject] = {
                    "subject": subject,
                    "total_sessions": 0,
                    "total_attempts": 0,
                    "correct_attempts": 0
                }
            subject_performance[subject]["total_sessions"] += 1
            
            session_attempts = self.attempts.get(session["session_id"], [])
            subject_performance[subject]["total_attempts"] += len(session_attempts)
            subject_performance[subject]["correct_attempts"] += sum(
                1 for a in session_attempts if a.get("is_correct", False)
            )
        
        for subject_data in subject_performance.values():
            if subject_data["total_attempts"] > 0:
                subject_data["accuracy"] = (
                    subject_data["correct_attempts"] / subject_data["total_attempts"] * 100
                )
            else:
                subject_data["accuracy"] = 0
        
        return {
            "overview": {
                "total_sessions": total_sessions,
                "completed_sessions": completed_sessions,
                "total_attempts": total_attempts,
                "overall_accuracy": round(accuracy, 2)
            },
            "subject_performance": list(subject_performance.values()),
            "user_skills": list(self.user_skills.values())
        }


storage = InMemoryStorage()

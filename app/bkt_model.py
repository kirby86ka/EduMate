from typing import Dict, Optional
from app.models import BKTParameters, DifficultyLevel, UserSkill
from app.database import db_manager
import logging

logger = logging.getLogger(__name__)


class BayesianKnowledgeTracing:
    def __init__(self, params: Optional[BKTParameters] = None):
        self.params = params or BKTParameters()
    
    def update_mastery(
        self,
        current_mastery: float,
        is_correct: bool
    ) -> float:
        p_transit = current_mastery * (1 - self.params.p_learn) + (1 - current_mastery) * self.params.p_learn
        
        if is_correct:
            p_correct_given_mastery = 1 - self.params.p_slip
            p_correct_given_not_mastery = self.params.p_guess
        else:
            p_correct_given_mastery = self.params.p_slip
            p_correct_given_not_mastery = 1 - self.params.p_guess
        
        p_correct = (p_transit * p_correct_given_mastery + 
                    (1 - p_transit) * p_correct_given_not_mastery)
        
        if p_correct == 0:
            return p_transit
        
        new_mastery = (p_transit * p_correct_given_mastery) / p_correct
        
        return max(0.0, min(1.0, new_mastery))
    
    def recommend_difficulty(self, mastery: float) -> DifficultyLevel:
        if mastery < 0.3:
            return DifficultyLevel.EASY
        elif mastery < 0.6:
            return DifficultyLevel.MEDIUM
        else:
            return DifficultyLevel.HARD
    
    async def update_user_skill(
        self,
        session_id: str,
        topic: str,
        subject: str,
        is_correct: bool,
        user_id: Optional[str] = None
    ) -> UserSkill:
        skills_collection = db_manager.get_collection("user_skills")
        
        existing_skill = await skills_collection.find_one({
            "session_id": session_id,
            "topic": topic
        })
        
        if existing_skill:
            current_mastery = existing_skill.get("mastery_probability", self.params.p_init)
            new_mastery = self.update_mastery(current_mastery, is_correct)
            
            await skills_collection.update_one(
                {"_id": existing_skill["_id"]},
                {
                    "$set": {"mastery_probability": new_mastery},
                    "$inc": {
                        "attempts_count": 1,
                        "correct_count": 1 if is_correct else 0
                    }
                }
            )
            
            existing_skill["mastery_probability"] = new_mastery
            existing_skill["attempts_count"] = existing_skill.get("attempts_count", 0) + 1
            existing_skill["correct_count"] = existing_skill.get("correct_count", 0) + (1 if is_correct else 0)
            
            return UserSkill(**existing_skill)
        else:
            new_mastery = self.update_mastery(self.params.p_init, is_correct)
            skill_data = {
                "session_id": session_id,
                "user_id": user_id,
                "subject": subject,
                "topic": topic,
                "mastery_probability": new_mastery,
                "attempts_count": 1,
                "correct_count": 1 if is_correct else 0
            }
            
            result = await skills_collection.insert_one(skill_data)
            skill_data["_id"] = result.inserted_id
            
            return UserSkill(**skill_data)
    
    async def get_topic_mastery(self, session_id: str) -> Dict[str, float]:
        skills_collection = db_manager.get_collection("user_skills")
        skills = await skills_collection.find({"session_id": session_id}).to_list(length=None)
        
        topic_mastery = {}
        for skill in skills:
            topic_mastery[skill["topic"]] = skill.get("mastery_probability", 0.5)
        
        return topic_mastery


bkt_model = BayesianKnowledgeTracing()

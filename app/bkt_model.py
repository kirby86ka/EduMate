from typing import Dict, Optional
from app.models import BKTParameters, DifficultyLevel
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
    
    def recommend_difficulty(self, mastery: float) -> str:
        """Return difficulty level as string (easy, medium, hard) based on mastery"""
        if mastery < 0.3:
            return "easy"
        elif mastery < 0.6:
            return "medium"
        else:
            return "hard"


bkt_model = BayesianKnowledgeTracing()

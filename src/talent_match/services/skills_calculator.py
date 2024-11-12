from typing import List

from talent_match.config.settings import get_settings
from talent_match.models.evaluation import SkillEvaluation
from talent_match.models.types import RelevanceLevel

settings = get_settings()

class SkillsCalculator:
    MIN_SKILLS = settings.MIN_SKILLS
    
    LEVEL_SCORES = {
        "BASIC": settings.SKILL_BASIC_SCORE,
        "INTERMEDIATE": settings.SKILL_INTERMEDIATE_SCORE,
        "ADVANCED": settings.SKILL_ADVANCED_SCORE
    }
    
    RELEVANCE_MULTIPLIERS = {
        RelevanceLevel.VERY_HIGH: settings.RELEVANCE_VERY_HIGH / 100,
        RelevanceLevel.HIGH: settings.RELEVANCE_HIGH / 100,
        RelevanceLevel.MEDIUM: settings.RELEVANCE_MEDIUM / 100,
        RelevanceLevel.LOW: settings.RELEVANCE_LOW / 100,
        RelevanceLevel.VERY_LOW: settings.RELEVANCE_VERY_LOW / 100,
        RelevanceLevel.NONE: settings.RELEVANCE_NONE / 100
    }
    
    @classmethod
    def calculate_skills_score(cls, skills: List[SkillEvaluation]) -> float:
        """
        Calcula la puntuación de habilidades considerando un mínimo necesario.
        
        Args:
            skills: Lista de habilidades evaluadas

        Returns:
            float: Puntuación entre 0 y 100
        """
        if not skills:
            return 0.0
            
        # Factor de penalización por número insuficiente de skills
        skills_factor = min(len(skills) / cls.MIN_SKILLS, 1.0)
        
        # Calcular puntuación para cada skill
        skill_scores = []
        for skill in skills:
            base_score = cls.LEVEL_SCORES[skill.level]
            relevance_multiplier = cls.RELEVANCE_MULTIPLIERS[skill.relevance]
            skill_scores.append(base_score * relevance_multiplier)
        

        # Calcular media de todas las puntuaciones
        avg_score = sum(skill_scores) / len(skill_scores)
        final_score = avg_score * skills_factor
        
        return round(final_score, 2)
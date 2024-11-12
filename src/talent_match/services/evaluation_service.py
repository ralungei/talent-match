from typing import List

from talent_match.config.settings import get_settings
from talent_match.models.evaluation import (
    CompleteEvaluation,
    EducationEvaluation,
    RelevantExperience,
    SkillEvaluation,
)
from talent_match.models.types import ScoreCalculator
from talent_match.services.experience_calculator import ExperienceCalculator
from talent_match.services.skills_calculator import SkillsCalculator

settings = get_settings()

class EvaluationService:
    """
    Servicio para calcular puntuaciones basadas en evaluaciones cualitativas.
    """
    
    @staticmethod
    def calculate_experience_score(experiences: List[RelevantExperience]) -> float:
        """
        Calcula la puntuación de experiencia usando el nuevo calculador especializado.
        
        Args:
            experiences: Lista de experiencias relevantes evaluadas

        Returns:
            float: Puntuación entre 0 y 100
        """
        return ExperienceCalculator.calculate_experience_score(experiences)
    
    @staticmethod
    def calculate_skills_score(skills: List[SkillEvaluation]) -> float:
        """
        Calcula la puntuación de habilidades basada en los niveles evaluados.
        
        El cálculo considera:
        - Nivel BASIC: 33.3 puntos
        - Nivel INTERMEDIATE: 66.6 puntos
        - Nivel ADVANCED: 100 puntos
        
        Args:
            skills: Lista de habilidades evaluadas

        Returns:
            float: Puntuación entre 0 y 100
        """
        return SkillsCalculator.calculate_skills_score(skills)

    
    @staticmethod
    def calculate_education_score(education: EducationEvaluation) -> float:
        """
        Calcula la puntuación de educación basada en el nivel de relevancia.
        
        La puntuación se basa en una escala predefinida:
        - NONE: 0 puntos
        - VERY_LOW: 20 puntos
        - LOW: 40 puntos
        - MEDIUM: 60 puntos
        - HIGH: 80 puntos
        - VERY_HIGH: 100 puntos
        
        Args:
            education: Evaluación de la formación académica

        Returns:
            float: Puntuación entre 0 y 100
        """
        return ScoreCalculator.relevance_to_score(education.relevance_level)
    
    def calculate_final_score(self, evaluation: CompleteEvaluation) -> float:
        """
        Calcula la puntuación final ponderando los diferentes aspectos evaluados.
        
        Args:
            evaluation: Evaluación completa del CV

        Returns:
            float: Puntuación final entre 0 y 100
        """
        # Calcular puntuaciones individuales
        exp_score = self.calculate_experience_score(evaluation.experiences)
        skills_score = self.calculate_skills_score(evaluation.skills)
        edu_score = self.calculate_education_score(evaluation.education)
        
        # Calcular puntuación final ponderada
        final_score = (
            exp_score * settings.EXPERIENCE_WEIGHT +
            skills_score * settings.SKILLS_WEIGHT +
            edu_score * settings.EDUCATION_WEIGHT
        )
        
        return round(final_score, 2)
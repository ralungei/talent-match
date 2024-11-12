from enum import Enum

from talent_match.config.settings import get_settings

settings = get_settings()

class ExperienceType(str, Enum):
    DIRECT = "DIRECT"
    RELATED = "RELATED"
    UNRELATED = "UNRELATED" 
    
class SkillLevel(str, Enum):
    BASIC = "BASIC"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"

class RelevanceLevel(str, Enum):
    """Niveles de relevancia para evaluaciones cualitativas"""
    NONE = "NONE"
    VERY_LOW = "VERY_LOW"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"

class ScoreCalculator:
    """Utilidad para convertir evaluaciones cualitativas en puntuaciones numéricas"""
    
    @staticmethod
    def relevance_to_score(level: RelevanceLevel) -> float:
        """Convierte un nivel de relevancia en una puntuación de 0 a 100"""
        scores = {
            RelevanceLevel.NONE: settings.RELEVANCE_NONE,
            RelevanceLevel.VERY_LOW: settings.RELEVANCE_VERY_LOW,
            RelevanceLevel.LOW: settings.RELEVANCE_LOW,
            RelevanceLevel.MEDIUM: settings.RELEVANCE_MEDIUM,
            RelevanceLevel.HIGH: settings.RELEVANCE_HIGH,
            RelevanceLevel.VERY_HIGH: settings.RELEVANCE_VERY_HIGH
        }
        return scores.get(level, 0.0)

    @staticmethod
    def skill_level_to_score(level: SkillLevel) -> float:
        """Convierte un nivel de habilidad en una puntuación de 0 a 100"""
        scores = {
            SkillLevel.BASIC: settings.SKILL_BASIC_SCORE,
            SkillLevel.INTERMEDIATE: settings.SKILL_INTERMEDIATE_SCORE,
            SkillLevel.ADVANCED: settings.SKILL_ADVANCED_SCORE
        }
        return scores.get(level, 0.0)

    @staticmethod
    def experience_type_to_score(type: ExperienceType) -> float:
        """Convierte un tipo de experiencia en una puntuación de 0 a 100"""
        scores = {
            ExperienceType.DIRECT: settings.DIRECT_SCORE,
            ExperienceType.RELATED: settings.RELATED_SCORE
        }
        return scores.get(type, 0.0)
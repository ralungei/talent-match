from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    OPENAI_TEMPERATURE: float = 0.1
    OPENAI_SEED: int = 42
    
    # App Config
    APP_NAME: str = "Talent Match"
    
    # Evaluation Weights
    EXPERIENCE_WEIGHT: float = 0.4
    SKILLS_WEIGHT: float = 0.3
    EDUCATION_WEIGHT: float = 0.3
    
    # Experience Config
    MAX_YEARS_FULL_SCORE: int = 5
    DIRECT_SCORE: float = 100.0
    RELATED_SCORE: float = 20.0
    RECENCY_BONUS: float = 0.2
    RECENCY_YEARS: int = 2
    DIRECT_EXPERIENCE_WEIGHT: float = 0.7
    RELATED_EXPERIENCE_WEIGHT: float = 0.3
    
    # Skills Config
    MIN_SKILLS: int = 5
    SKILL_BASIC_SCORE: float = 33.3
    SKILL_INTERMEDIATE_SCORE: float = 66.6
    SKILL_ADVANCED_SCORE: float = 100.0
    
    # Relevance Multipliers (0-100)
    RELEVANCE_NONE: float = 0.0
    RELEVANCE_VERY_LOW: float = 20.0
    RELEVANCE_LOW: float = 40.0
    RELEVANCE_MEDIUM: float = 60.0
    RELEVANCE_HIGH: float = 80.0
    RELEVANCE_VERY_HIGH: float = 100.0
    
    # Education Scores
    EDUCATION_NONE: float = 0.0
    EDUCATION_VERY_LOW: float = 20.0
    EDUCATION_LOW: float = 40.0
    EDUCATION_MEDIUM: float = 60.0
    EDUCATION_HIGH: float = 80.0
    EDUCATION_VERY_HIGH: float = 100.0

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
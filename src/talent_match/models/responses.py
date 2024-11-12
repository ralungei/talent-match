from typing import List

from pydantic import BaseModel

from .evaluation import (
    EducationEvaluation,
    RelevantExperience,
    SkillEvaluation,
    Summary,
)


class ExperienceResponse(BaseModel):
    """Modelo de respuesta para el análisis de experiencia"""
    experiences: List[RelevantExperience]

class SkillsResponse(BaseModel):
    """Modelo de respuesta para el análisis de habilidades"""
    skills: List[SkillEvaluation]

class EducationResponse(BaseModel):
    """Modelo de respuesta para el análisis de educación"""
    education: EducationEvaluation

class SummaryResponse(BaseModel):
    """Modelo de respuesta para el resumen general"""
    summary: Summary
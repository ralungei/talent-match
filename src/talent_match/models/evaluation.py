from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel

from .types import ExperienceType, RelevanceLevel, SkillLevel


class ExperienceDates(BaseModel):
    start_date: str 
    end_date: Optional[str] = None  
    
    @property
    def start(self) -> date:
        """Convierte start_date a objeto date"""
        return datetime.strptime(self.start_date, "%d-%m-%Y").date()
    
    @property
    def end(self) -> date:
        """Convierte end_date a objeto date o retorna fecha actual"""
        if self.end_date:
            return datetime.strptime(self.end_date, "%d-%m-%Y").date()
        return date.today()
    
    def calculate_duration(self) -> float:
        duration = (self.end - self.start).days / 365.25
        return round(duration, 2)
    
    def format_duration(self) -> str:
        years = self.calculate_duration()
        if years >= 1:
            return f"{int(years)} año{'s' if years != 1 else ''}"
        months = int(years * 12)
        return f"{months} mes{'es' if months != 1 else ''}"
    
class RelevantExperience(BaseModel):
    position: str
    company: str
    dates: ExperienceDates
    relevance_explanation: str
    match_type: ExperienceType
    relevant_skills: List[str]
    
    @property
    def duration_years(self) -> float:
        """Retorna la duración en años para cálculos"""
        return self.dates.calculate_duration()
    
    @property
    def duration_text(self) -> str:
        """Retorna la duración formateada para mostrar"""
        return self.dates.format_duration()

class SkillEvaluation(BaseModel):
    skill_name: str
    relevance_explanation: str
    level: SkillLevel
    relevance: RelevanceLevel 
    

class EducationEvaluation(BaseModel):
    relevance_level: RelevanceLevel
    relevant_courses: List[str]
    education_fit: str

class Summary(BaseModel):
    strengths: List[str]
    areas_of_improvement: List[str]
    overall_assessment: str
    fit_score: float  

class CompleteEvaluation(BaseModel):
    experiences: List[RelevantExperience]
    skills: List[SkillEvaluation]
    education: EducationEvaluation
    summary: Summary
import math
from datetime import date
from typing import List

from talent_match.config.settings import get_settings
from talent_match.models.evaluation import RelevantExperience

settings = get_settings()


class ExperienceCalculator:
    """
    Servicio para calcular puntuaciones de experiencia con una lógica mejorada
    que considera:
    - Tipo de experiencia (DIRECT/RELATED)
    - Duración acumulada por tipo
    - Bonus por experiencia reciente
    - Penalización por gaps
    - Ignora experiencias UNRELATED
    """

    @classmethod
    def calculate_experience_score(cls, experiences: List[RelevantExperience]) -> float:
        """
        Calcula la puntuación de experiencia con una lógica mejorada.

        La puntuación se calcula:
        1. Separando y acumulando años por tipo de experiencia
        2. Aplicando una curva logarítmica más suave
        3. Añadiendo bonus por experiencia reciente
        4. Combinando los resultados con pesos apropiados

        Returns:
            float: Puntuación entre 0 y 100
        """
        if not experiences:
            return 0.0

        relevant_experiences = [
            exp for exp in experiences
            if exp.match_type in ["DIRECT", "RELATED"]
        ]

        if not relevant_experiences:
            return 0.0

        # Acumular años por tipo
        direct_years = 0.0
        related_years = 0.0
        recent_experience = False

        current_date = date.today()

        for exp in relevant_experiences:
            duration = exp.duration_years

            # Verificar si es experiencia reciente
            if not exp.dates.end_date:  # Trabajo actual
                recent_experience = True
            elif (current_date - exp.dates.end).days <= settings.RECENCY_YEARS * 365:
                recent_experience = True

            # Acumular años por tipo
            if exp.match_type == "DIRECT":
                direct_years += duration
            elif exp.match_type == "RELATED":
                related_years += duration

        # Calcular puntuación base por tipo usando curva logarítmica suave
        direct_score = cls._calculate_type_score(
            direct_years,
            settings.DIRECT_SCORE
        )

        related_score = cls._calculate_type_score(
            related_years,
            settings.RELATED_SCORE
        )

        # Combinar puntuaciones con pesos
        combined_score = (
            direct_score * settings.DIRECT_EXPERIENCE_WEIGHT +
            related_score * settings.RELATED_EXPERIENCE_WEIGHT
        )

        # Aplicar bonus por experiencia reciente
        if recent_experience:
            combined_score = min(100, combined_score *
                                 (1 + settings.RECENCY_BONUS))

        return round(combined_score, 2)

    @classmethod
    def _calculate_type_score(cls, years: float, base_score: float) -> float:
        """
        Calcula la puntuación para un tipo específico de experiencia
        usando una curva logarítmica más suave.
        """
        if years <= 0:
            return 0.0

        # Usar log(x + 1) para una curva más suave
        # y normalizar a MAX_YEARS_FOR_FULL_SCORE
        factor = min(
            math.log(years + 1) / math.log(settings.MAX_YEARS_FULL_SCORE + 1),
            1.0
        )

        return base_score * factor

from ..base import BasePrompt


class EducationPrompt(BasePrompt):
    template = """
    Evalúa la formación del candidato para el puesto de <${job_title}>.

    Analiza:
    1. Relevancia de la formación académica
    2. Cursos o certificaciones relevantes
    3. Ajuste de la formación con los requisitos del puesto
    4. Formación complementaria valiosa

    La relevancia debe ser uno de estos valores:
    - NONE: La formación no tiene ninguna relación con el puesto
    - VERY_LOW: La formación tiene muy poca relación con el puesto
    - LOW: La formación tiene alguna relación pero no es la ideal
    - MEDIUM: La formación es moderadamente relevante
    - HIGH: La formación es bastante relevante
    - VERY_HIGH: La formación es extremadamente relevante

    La salida debe ser un JSON con esta estructura exacta:
    {
        "education": {
            "education_fit": str,
            "relevant_courses": List[str],
            "relevance_level": "NONE" | "VERY_LOW" | "LOW" | "MEDIUM" | "HIGH" | "VERY_HIGH"
        }
    }
    """
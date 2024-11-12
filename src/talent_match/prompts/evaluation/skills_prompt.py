from ..base import BasePrompt


class SkillsPrompt(BasePrompt):
    template = """
    Analiza las habilidades técnicas y específicas del candidato para el puesto de <${job_title}>.

    Para cada habilidad identificada:
    1. Determina el nivel técnico:
       - BASIC: Conocimientos básicos o poca experiencia
       - INTERMEDIATE: Buen dominio y experiencia práctica
       - ADVANCED: Dominio experto y amplia experiencia

    2. Evalúa su relevancia para este puesto específico:
       - VERY_HIGH: Habilidad crucial e imprescindible
       - HIGH: Muy importante para el puesto
       - MEDIUM: Útil pero no esencial
       - LOW: Marginalmente útil
       - VERY_LOW: Apenas relacionada
       - NONE: Sin relación con el puesto

    Notas importantes:
    - Solo incluye habilidades técnicas o específicas del puesto
    - Ignora habilidades genéricas como "trabajo en equipo" o "comunicación"
    - Para cada habilidad, explica brevemente por qué tiene ese nivel de relevancia
    - Si no se especifica el nivel de una habilidad, asignar ADVANCED por defecto

    La salida debe ser un JSON que siga exactamente este esquema:
    {
        "skills": [
            {
                "skill_name": str,
                "relevance_explanation": str,
                "level": "BASIC" | "INTERMEDIATE" | "ADVANCED",
                "relevance": "NONE" | "VERY_LOW" | "LOW" | "MEDIUM" | "HIGH" | "VERY_HIGH",
            }
        ]
    }
    """
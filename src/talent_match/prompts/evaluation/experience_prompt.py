from ..base import BasePrompt


class ExperiencePrompt(BasePrompt):
    template = """
    Analiza la experiencia laboral del candidato para el puesto de <${job_title}>.

    Para cada experiencia laboral:
    1. Identifica:
       - Cargo/posición
       - Empresa
       - Fechas de inicio y fin en formato DD-MM-YYYY (usa null si es trabajo actual)
       - Habilidades relevantes para el puesto
       - Nivel de relevancia para el puesto

    2. Clasifica como:
       - DIRECT: Mismo puesto o responsabilidades muy similares
       - RELATED: Diferentes puestos pero con habilidades aplicables
       - UNRELATED: Experiencia no relacionada con el puesto

    La salida debe ser un JSON que siga exactamente este esquema:
    {
        "experiences": [
            {
                "position": str,
                "company": str,
                "dates": {
                    "start_date": "DD-MM-YYYY",
                    "end_date": "DD-MM-YYYY" | null  # null para trabajo actual
                },
                "relevance_explanation": str,
                "match_type": "DIRECT" | "RELATED" | "UNRELATED",
                "relevant_skills": List[str]
            }
        ]
    }
    """
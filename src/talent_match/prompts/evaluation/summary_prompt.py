from ..base import BasePrompt


class SummaryPrompt(BasePrompt):
    template = """
    Genera un resumen ejecutivo de la evaluación del candidato para el puesto de <${job_title}>.

    Basándote en:
    - Experiencia laboral relevante
    - Habilidades clave identificadas
    - Formación y certificaciones

    La salida debe ser un JSON que siga exactamente este esquema:
    {
        "summary": {
            "overall_assessment": str,
            "strengths": List[str],
            "areas_of_improvement": List[str]
        }
    }
    """
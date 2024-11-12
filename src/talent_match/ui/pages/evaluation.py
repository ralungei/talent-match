import asyncio
import json

import streamlit as st

from talent_match.config.settings import get_settings
from talent_match.services.openai_service import OpenAIService
from talent_match.ui.components.metrics import display_key_metrics
from talent_match.ui.components.sections import display_summary_section

settings = get_settings()

def initialize_session_state():
    if 'api_key' not in st.session_state:
        st.session_state.api_key = settings.OPENAI_API_KEY

async def analyze_cv(cv_text: str, job_title: str, api_key: str):
    settings.OPENAI_API_KEY = api_key
    service = OpenAIService()
    return await service.analyze_cv(cv_text, job_title)

def format_output_json(evaluation):
    """
    Formatea la evaluación en el JSON específico requerido.
    Solo incluye experiencias directamente relacionadas.
    """
    # Filtra y formatea solo la experiencia directa
    direct_experience = [
        {
            "puesto": exp.position,
            "empresa": exp.company,
            "duracion": exp.dates.format_duration()
        }
        for exp in evaluation.experiences
        if exp.match_type == "DIRECT"
    ]
    
    return {
        "puntuacion": evaluation.summary.fit_score,
        "experiencia_relevante": direct_experience,
        "descripcion": evaluation.summary.overall_assessment
    }

def display_json_output(evaluation):
    """
    Muestra y permite descargar el JSON de salida.
    """
    st.header("🔍 Resultado en formato JSON")
    
    output_json = format_output_json(evaluation)
    
    # Mostrar el JSON formateado
    st.json(output_json)
    
    # Botón para descargar el JSON
    json_str = json.dumps(output_json, ensure_ascii=False, indent=2)
    st.download_button(
        label="⬇️ Descargar JSON",
        data=json_str,
        file_name="evaluacion.json",
        mime="application/json",
    )

def display_evaluation_results(evaluation):
    st.write("")  
    st.divider() 

    st.title("📊 Evaluación del CV")
    display_key_metrics(evaluation)
    display_summary_section(evaluation)

    st.divider()
    display_json_output(evaluation)

def main():
    initialize_session_state()
    
    st.title("🎯 Talent Match")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### ¿Qué puesto estás buscando?")
        job_title = st.text_input(
            label="Puesto de trabajo",
            placeholder="Ej: Data Scientist...",
            key="job_title",
            label_visibility="collapsed"
        )
        
        st.write("")
        
        evaluate_button = st.button(
            "Evaluar CV",
            type="primary",
            use_container_width=True,
            disabled=not (job_title and st.session_state.get('cv_text', ''))
        )
    
    with col2:
        st.markdown("### CV del candidato")
        cv_text = st.text_area(
            label="Contenido del CV",
            placeholder="Pega aquí el contenido del CV...",
            height=200,
            key="cv_text",
            label_visibility="collapsed" 
        )
    
    if evaluate_button:
        try:
            with st.spinner("Evaluando..."):
                evaluation = asyncio.run(
                    analyze_cv(cv_text, job_title, st.session_state.api_key)
                )
                display_evaluation_results(evaluation)
        except Exception as e:
            st.error(f"Error durante la evaluación: {str(e)}")

if __name__ == "__main__":
    main()
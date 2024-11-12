import streamlit as st

from talent_match.config.settings import get_settings
from talent_match.models.types import RelevanceLevel
from talent_match.services.evaluation_service import EvaluationService

settings = get_settings()

def get_metric_labels():
    settings = get_settings()
    return {
        'experience': f"Experiencia ({settings.EXPERIENCE_WEIGHT * 100:.0f}%)",
        'skills': f"Habilidades ({settings.SKILLS_WEIGHT * 100:.0f}%)",
        'education': f"Educación ({settings.EDUCATION_WEIGHT * 100:.0f}%)"
    }

def get_level_score(level: str) -> float:
    scores = {
        "BASIC": settings.SKILL_BASIC_SCORE,
        "INTERMEDIATE": settings.SKILL_INTERMEDIATE_SCORE,
        "ADVANCED": settings.SKILL_ADVANCED_SCORE
    }
    return scores.get(level, 0.0)

def get_relevance_multiplier(relevance: RelevanceLevel) -> float:
    multipliers = {
        RelevanceLevel.VERY_HIGH: settings.RELEVANCE_VERY_HIGH / 100,
        RelevanceLevel.HIGH: settings.RELEVANCE_HIGH / 100,
        RelevanceLevel.MEDIUM: settings.RELEVANCE_MEDIUM / 100,
        RelevanceLevel.LOW: settings.RELEVANCE_LOW / 100,
        RelevanceLevel.VERY_LOW: settings.RELEVANCE_VERY_LOW / 100,
        RelevanceLevel.NONE: settings.RELEVANCE_NONE / 100
    }
    return multipliers.get(relevance, 0.0)

def get_relevance_label(level: RelevanceLevel) -> str:
    labels = {
        RelevanceLevel.NONE: "NINGUNA",
        RelevanceLevel.VERY_LOW: "MUY BAJA",
        RelevanceLevel.LOW: "BAJA",
        RelevanceLevel.MEDIUM: "MEDIA",
        RelevanceLevel.HIGH: "ALTA",
        RelevanceLevel.VERY_HIGH: "MUY ALTA"
    }
    return labels.get(level, str(level).split('.')[-1])

def display_key_metrics(evaluation):
    # Calculamos las puntuaciones individuales
    evaluation_service = EvaluationService()
    exp_score = evaluation_service.calculate_experience_score(evaluation.experiences)
    skills_score = evaluation_service.calculate_skills_score(evaluation.skills)
    edu_score = evaluation_service.calculate_education_score(evaluation.education)
    final_score = evaluation.summary.fit_score
    
    # Crear columnas con diferentes anchos (2 para la primera, 1 para las demás)
    col_final, col_exp, col_skills, col_edu = st.columns([2, 1, 1, 1])
    
    with col_final:
        st.metric(
            "Puntuación Final",
            f"{final_score:.1f}%",
            help="Puntuación ponderada considerando todos los factores"
        )

    labels = get_metric_labels()
    with col_exp:
        st.metric(
            labels['experience'],
            f"{exp_score:.1f}/100",
            help="Puntuación base y contribución ponderada"
        )
    with col_skills:
        st.metric(
            labels['skills'],
            f"{skills_score:.1f}/100",
            help="Puntuación base y contribución ponderada"
        )
    with col_edu:
        st.metric(
            labels['education'],
            f"{edu_score:.1f}/100",
            help="Puntuación base y contribución ponderada"
        )
    
    # Tabs para el desglose detallado
    tab_exp, tab_skills, tab_edu = st.tabs([
        "💼 Desglose Experiencia",
        "🛠️ Desglose Habilidades",
        "📚 Desglose Educación"
    ])
    
    with tab_exp:
        st.subheader("Desglose de Experiencia")
        if evaluation.experiences:
            for exp in evaluation.experiences:
                if exp.match_type == "UNRELATED":
                    points = 0
                else:
                    points = settings.DIRECT_SCORE if exp.match_type == "DIRECT" else settings.RELATED_SCORE

                    
                with st.expander(f"📋 {exp.position} en {exp.company}", expanded=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.info("Experiencia directa" if exp.match_type == "DIRECT" else "Experiencia relacionada" if exp.match_type == "RELATED" else "Experiencia no relacionada")
                        st.markdown(f"**⏱️ Duración:** {exp.duration_text}")
                    with col2:
                        st.metric("Puntos", points)
                        st.write("DIRECTO" if exp.match_type == "DIRECT" else ("RELACIONADO" if exp.match_type == "RELATED" else "NO RELACIONADO"))

                    if exp.relevant_skills:
                        st.markdown("**🛠️ Habilidades relevantes:**")
                        st.write(", ".join(exp.relevant_skills))
                    
                    st.info(exp.relevance_explanation)
        else:
            st.warning("No se encontraron experiencias relevantes")
            
        explanation = f"""
        <div style="background-color: rgb(46 46 46); color: white; padding: 1em; border-radius: 20px;">
        <strong>Cálculo:</strong><br>
        - Experiencia DIRECTA: {settings.DIRECT_SCORE} puntos base<br>
        - Experiencia RELACIONADA: {settings.RELATED_SCORE} puntos base<br>
        - Experiencia NO RELACIONADA: 0 puntos<br>
        - Factor duración: min(años_experiencia / {settings.MAX_YEARS_FULL_SCORE}, 1)<br>
        * Se considera {settings.MAX_YEARS_FULL_SCORE} años como experiencia máxima (100%)<br>
        * Ejemplo: 3 años = 0.6 (60% del máximo), {settings.MAX_YEARS_FULL_SCORE+1} años = 1.0 (100% del máximo)<br>
        - Peso experiencia directa: {settings.DIRECT_EXPERIENCE_WEIGHT}<br>
        - Peso experiencia relacionada: {settings.RELATED_EXPERIENCE_WEIGHT}<br>
        - Bonus por experiencia reciente: +{int(settings.RECENCY_BONUS * 100)}%<br>
        - Puntuación final: (suma de puntuaciones ponderadas) × {settings.EXPERIENCE_WEIGHT}
        </div>
        """
        st.markdown(explanation, unsafe_allow_html=True)

    with tab_skills:
        st.subheader("Desglose de Habilidades")
        if evaluation.skills:            
            # Mostrar el número total de habilidades
            total_skills = len(evaluation.skills)
            st.metric(
                "Número de habilidades", 
                f"{total_skills}/5", 
            )
            
            # Mostrar cada habilidad
            for skill in evaluation.skills:
                with st.expander(f"🛠️ {skill.skill_name}", expanded=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.info(f"**Nivel:** {skill.level}")
                        st.success(f"**Relevancia:** {get_relevance_label(skill.relevance)}")
                        st.write(f"**Explicación:** {skill.relevance_explanation}")
                    with col2:
                        level_score = get_level_score(skill.level)
                        relevance_mult = get_relevance_multiplier(skill.relevance)

                        
                        skill_score = level_score * relevance_mult
                        st.metric(
                            "Puntuación", 
                            f"{skill_score:.1f}",
                            help=f"Nivel ({level_score}) × Relevancia ({relevance_mult:.1f})"
                        )
            st.markdown("""
            <div style="background-color: rgb(46 46 46); color: white; padding: 1em; border-radius: 20px;">
            <strong>Sistema de puntuación:</strong><br>
            - Se evalúan todas las habilidades según nivel y relevancia<br>
            - Nivel: BÁSICO (33.3), INTERMEDIO (66.6), AVANZADO (100)<br>
            - La relevancia actúa como multiplicador: MUY ALTA (1.0) a NINGUNA (0.0)<br>
            - Se requiere un mínimo de 5 habilidades para puntuación máxima
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("No se encontraron habilidades evaluadas")

    with tab_edu:
        st.subheader("Desglose de Educación")
        relevance_score = evaluation_service.calculate_education_score(evaluation.education)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"**Nivel de relevancia:** {get_relevance_label(evaluation.education.relevance_level)}")
            if evaluation.education.relevant_courses:
                st.markdown("**📖 Cursos relevantes:**")
                for course in evaluation.education.relevant_courses:
                    st.success(f"- {course}")
            st.info(evaluation.education.education_fit)
        with col2:
            st.metric("Puntos", f"{relevance_score:.1f}")
            st.progress(relevance_score / 100)
            
        st.markdown("""
        <div style="background-color: rgb(46 46 46); color: white; padding: 1em; border-radius: 20px;">
        <strong>Cálculo por nivel de relevancia:</strong><br>
        - NONE: 0 puntos<br>
        - VERY_LOW: 20 puntos<br>
        - LOW: 40 puntos<br>
        - MEDIUM: 60 puntos<br>
        - HIGH: 80 puntos<br>
        - VERY_HIGH: 100 puntos<br>
        - Puntuación final: Puntos × 0.3
        </div>
        """, unsafe_allow_html=True)
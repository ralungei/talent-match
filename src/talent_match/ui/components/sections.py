import streamlit as st

from talent_match.models.types import RelevanceLevel, ScoreCalculator


def display_summary_section(evaluation):
    st.header("General")
    st.markdown(evaluation.summary.overall_assessment)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Fortalezas")
        for strength in evaluation.summary.strengths:
            st.success(strength)
    
    with col2:
        st.subheader("Áreas de mejora")
        for area in evaluation.summary.areas_of_improvement:
            st.error(area)

def display_experience_section(evaluation):
    st.header("💼 Experiencia relevante")
    
    for exp in evaluation.experiences:
        with st.expander(f"📋 {exp.position} en {exp.company}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.info(exp.match_type)
            with col2:
                st.markdown(f"**⏱️ Duración:** {exp.duration_text}") 
            
            if exp.relevant_skills:
                st.markdown("**🛠️ Habilidades relevantes:**")
                st.write(", ".join(exp.relevant_skills))
            
            st.info(exp.relevance_explanation)

def display_skills_section(evaluation):
    st.header("🛠️ Evaluación de habilidades")
    
    for skill in evaluation.skills:
        with st.expander(f"{skill.skill_name}"):
            st.info(f"Nivel: {skill.level}")
            st.write(f"Relevancia: {skill.relevance}")
            st.write(f"Explicación: {skill.relevance_explanation}")

def display_education_section(evaluation):
    st.header("📚 Evaluación educativa")
    
    relevance_score = ScoreCalculator.relevance_to_score(evaluation.education.relevance_level)
    st.progress(relevance_score / 100)
    st.metric("Relevancia educativa", f"{relevance_score}%")
    
    st.subheader("📖 Cursos relevantes")
    for course in evaluation.education.relevant_courses:
        st.info(course)
    
    st.info(evaluation.education.education_fit)
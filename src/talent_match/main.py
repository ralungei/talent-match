import streamlit as st

from talent_match.ui.pages.evaluation import main as evaluation_main


def setup_page_config():
    """Configuración inicial de la página de Streamlit"""
    st.set_page_config(
        page_title="CV Evaluator",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def setup_sidebar():
    """Configura la barra lateral con el campo de API key"""
    st.sidebar.title("Configuración")
    
    # Campo para la API key
    api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        value=st.session_state.get('api_key', ''),
        key="api_key_input"
    )
    
    # Actualizar la API key en session state cuando cambie
    if api_key:
        st.session_state.api_key = api_key
        
def main():
    """Función principal de la aplicación"""
    setup_page_config()
    setup_sidebar()
    evaluation_main()

if __name__ == "__main__":
    main()
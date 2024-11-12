def get_skill_level_style(level: str) -> dict:
    """Retorna los estilos CSS para cada nivel de habilidad"""
    styles = {
        "BASIC": {
            "background": "linear-gradient(90deg, #9ec9e5 0%, #c4e0f3 100%)",
            "color": "#1a365d",
            "border": "1px solid #9ec9e5"
        },
        "INTERMEDIATE": {
            "background": "linear-gradient(90deg, #4393c3 0%, #6baed6 100%)",
            "color": "white",
            "border": "1px solid #4393c3"
        },
        "ADVANCED": {
            "background": "linear-gradient(90deg, #2166ac 0%, #4393c3 100%)",
            "color": "white",
            "border": "1px solid #2166ac"
        }
    }
    return styles.get(level, {})

def get_skill_level_label(level: str) -> str:
    """Convierte el nivel técnico en una etiqueta amigable"""
    labels = {
        "BASIC": "Nivel básico",
        "INTERMEDIATE": "Nivel intermedio",
        "ADVANCED": "Nivel avanzado"
    }
    return labels.get(level, level)

def get_experience_type_style(type: str) -> dict:
    """Retorna los estilos CSS para cada tipo de experiencia"""
    styles = {
        "DIRECT": {
            "background": "linear-gradient(90deg, #74c476 0%, #a1d99b 100%)",
            "color": "#1a365d",
            "border": "1px solid #74c476"
        },
        "RELATED": {
            "background": "linear-gradient(90deg, #fd8d3c 0%, #fdae6b 100%)",
            "color": "#1a365d",
            "border": "1px solid #fd8d3c"
        },
        "UNRELATED": {
            "background": "linear-gradient(90deg, #e0e0e0 0%, #f0f0f0 100%)",
            "color": "#666666",
            "border": "1px solid #e0e0e0"
        }
    }
    return styles.get(type, {})

def get_experience_type_label(type: str) -> str:
    """Convierte el tipo de experiencia en una etiqueta amigable"""
    labels = {
        "DIRECT": "Experiencia directa",
        "RELATED": "Experiencia relacionada",
        "UNRELATED": "Experiencia no relacionada"
    }
    return labels.get(type, type)

def style_tag(text: str, style: dict) -> str:
    """Genera un HTML tag estilizado"""
    style_str = '; '.join([f"{k}: {v}" for k, v in style.items()])
    return f"""
        <span style="
            {style_str};
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 0.9em;
            font-weight: 500;
            display: inline-block;
            margin: 2px 4px;
        ">
            {text}
        </span>
    """

def style_skill_tag(skill_name: str) -> str:
    """Genera un HTML tag estilizado para una habilidad"""
    return f"""
        <span style="
            background-color: #e6f3ff;
            color: #1a365d;
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 0.9em;
            font-weight: 500;
            display: inline-block;
            margin: 2px 4px;
            border: 1px solid #c5e1f9;
        ">
            {skill_name}
        </span>
    """
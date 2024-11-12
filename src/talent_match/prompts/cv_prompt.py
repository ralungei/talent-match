from .base import BasePrompt


class CVPrompt(BasePrompt):
    template = """Por favor, analiza el siguiente CV:

<cv_content>
${cv_text}
</cv_content>"""
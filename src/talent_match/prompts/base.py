from string import Template
from typing import Any, Dict


class BasePrompt:
    """Base class for all prompts"""
    
    template: str = ""
    
    @classmethod
    def format(cls, **kwargs: Dict[str, Any]) -> str:
        return Template(cls.template).safe_substitute(**kwargs)
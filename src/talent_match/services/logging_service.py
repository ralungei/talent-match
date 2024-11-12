import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4


class CVLoggingService:
    """Service for logging CV analysis results"""
    
    def __init__(self, base_log_dir: str = "logs/cv_analysis"):
        """
        Initialize the logging service
        
        Args:
            base_log_dir: Base directory for storing logs
        """
        self.base_log_dir = Path(base_log_dir)
        self.current_session: Optional[str] = None
        self._ensure_base_dir()
    
    def _ensure_base_dir(self):
        """Ensure the base log directory exists"""
        self.base_log_dir.mkdir(parents=True, exist_ok=True)
    
    def start_session(self, job_title: str, cv_text: str) -> str:
        """
        Start a new logging session for a CV analysis
        
        Args:
            job_title: The job title being analyzed for
            cv_text: The CV text being analyzed
            
        Returns:
            session_id: Unique identifier for the session
        """
        # Generate unique session ID
        session_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}"
        self.current_session = session_id
        
        # Create session directory
        session_dir = self.base_log_dir / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        
        # Save initial session info
        session_info = {
            "session_id": session_id,
            "job_title": job_title,
            "timestamp": datetime.now().isoformat(),
            "cv_text": cv_text
        }
        
        self._save_json(
            session_dir / "session_info.json",
            session_info
        )
        
        return session_id
    
    def log_prompt_result(self, 
                         prompt_type: str,
                         prompt_text: str,
                         response: Dict[str, Any],
                         messages: List[Dict[str, str]] = None,
                         session_id: Optional[str] = None):
        """
        Log the result of a prompt analysis
        
        Args:
            prompt_type: Type of analysis (experience, skills, education, summary)
            prompt_text: The actual prompt text used
            response: The response received from the model
            session_id: Optional session ID (uses current session if not provided)
        """
        if not session_id and not self.current_session:
            raise ValueError("No active session and no session_id provided")
        
        session_id = session_id or self.current_session
        prompt_dir = self.base_log_dir / session_id / "prompts"
        prompt_dir.mkdir(exist_ok=True)
        
        # Create prompt result log
        prompt_result = {
            "timestamp": datetime.now().isoformat(),
            "prompt_type": prompt_type,
            "prompt_text": prompt_text,
            "messages": messages, 
            "response": response
        }
        
        self._save_json(
            prompt_dir / f"{prompt_type}_result.json",
            prompt_result
        )
    
    def log_final_evaluation(self, 
                           evaluation: Dict[str, Any],
                           session_id: Optional[str] = None):
        """
        Log the final complete evaluation
        
        Args:
            evaluation: The complete evaluation result
            session_id: Optional session ID (uses current session if not provided)
        """
        if not session_id and not self.current_session:
            raise ValueError("No active session and no session_id provided")
            
        session_id = session_id or self.current_session
        session_dir = self.base_log_dir / session_id
        
        self._save_json(
            session_dir / "final_evaluation.json",
            evaluation
        )
    
    def _save_json(self, path: Path, data: Dict[str, Any]):
        """Save data as JSON with consistent formatting"""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, 
                     f,
                     ensure_ascii=False, 
                     indent=2,
                     default=str)
    
    @classmethod
    def load_session(cls, session_id: str, base_log_dir: str = "logs/cv_analysis") -> Dict[str, Any]:
        """
        Load a complete session's data
        
        Args:
            session_id: ID of the session to load
            base_log_dir: Base directory where logs are stored
            
        Returns:
            Dict containing all session data
        """
        base_dir = Path(base_log_dir)
        session_dir = base_dir / session_id
        
        if not session_dir.exists():
            raise ValueError(f"Session {session_id} not found")
        
        # Load session info
        with open(session_dir / "session_info.json", 'r', encoding='utf-8') as f:
            session_data = json.load(f)
        
        # Load prompt results
        prompt_dir = session_dir / "prompts"
        if prompt_dir.exists():
            prompt_results = {}
            for prompt_file in prompt_dir.glob("*_result.json"):
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    prompt_type = prompt_file.stem.replace("_result", "")
                    prompt_results[prompt_type] = json.load(f)
            session_data["prompt_results"] = prompt_results
        
        # Load final evaluation if exists
        final_eval_path = session_dir / "final_evaluation.json"
        if final_eval_path.exists():
            with open(final_eval_path, 'r', encoding='utf-8') as f:
                session_data["final_evaluation"] = json.load(f)
        
        return session_data
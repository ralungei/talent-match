from concurrent.futures import ThreadPoolExecutor

from openai import OpenAI

from talent_match.config.settings import get_settings
from talent_match.models.evaluation import CompleteEvaluation, Summary
from talent_match.models.responses import (
    EducationResponse,
    ExperienceResponse,
    SkillsResponse,
    SummaryResponse,
)
from talent_match.prompts.cv_prompt import CVPrompt
from talent_match.prompts.evaluation.education_prompt import EducationPrompt
from talent_match.prompts.evaluation.experience_prompt import ExperiencePrompt
from talent_match.prompts.evaluation.skills_prompt import SkillsPrompt
from talent_match.prompts.evaluation.summary_prompt import SummaryPrompt
from talent_match.services.evaluation_service import EvaluationService
from talent_match.services.logging_service import CVLoggingService

settings = get_settings()


class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.executor = ThreadPoolExecutor(max_workers=3)
        self.evaluation_service = EvaluationService()
        self.logging_service = CVLoggingService()

    async def analyze_cv(self, cv_text: str, job_title: str) -> CompleteEvaluation:
        # Start logging session
        session_id = self.logging_service.start_session(job_title, cv_text)

        # Create futures for parallel execution
        experience_future = self.executor.submit(
            self._analyze_experience, cv_text, job_title)
        skills_future = self.executor.submit(
            self._analyze_skills, cv_text, job_title)
        education_future = self.executor.submit(
            self._analyze_education, cv_text, job_title)

        # Wait for all futures to complete
        experience_result = experience_future.result()
        skills_result = skills_future.result()
        education_result = education_future.result()

        # Create initial evaluation without summary
        evaluation = CompleteEvaluation(
            experiences=experience_result,
            skills=skills_result,
            education=education_result,
            summary=Summary(
                overall_assessment="",
                strengths=[],
                areas_of_improvement=[],
                fit_score=0.0
            )
        )

        # Calculate score using evaluation service
        fit_score = self.evaluation_service.calculate_final_score(evaluation)

        # Generate summary with calculated score
        summary = self._generate_summary(
            cv_text,
            job_title,
            evaluation,
            fit_score
        )

        # Update evaluation with summary
        evaluation.summary = summary

        # Log final evaluation
        self.logging_service.log_final_evaluation(
            evaluation.dict(),
            session_id=session_id
        )

        return evaluation

    def _analyze_experience(self, cv_text: str, job_title: str):
        prompt = ExperiencePrompt.format(job_title=job_title)

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": CVPrompt.format(cv_text=cv_text)}
        ]

        completion = self.client.beta.chat.completions.parse(
            model=settings.OPENAI_MODEL,
            messages=messages,
            response_format=ExperienceResponse,
            seed=settings.OPENAI_SEED,
            temperature=settings.OPENAI_TEMPERATURE
        )

        message = completion.choices[0].message
        if message.parsed:
            # Log prompt result
            self.logging_service.log_prompt_result(
                prompt_type="experience",
                prompt_text=prompt,
                response=message.parsed.dict(),
                messages=messages
            )
            return message.parsed.experiences
        else:
            raise ValueError(
                f"Failed to parse experience response: {message.refusal}")

    def _analyze_skills(self, cv_text: str, job_title: str):
        prompt = SkillsPrompt.format(job_title=job_title)

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": CVPrompt.format(cv_text=cv_text)}
        ]

        completion = self.client.beta.chat.completions.parse(
            model=settings.OPENAI_MODEL,
            messages=messages,
            response_format=SkillsResponse,
            seed=settings.OPENAI_SEED,
            temperature=settings.OPENAI_TEMPERATURE
        )

        message = completion.choices[0].message
        if message.parsed:
            # Log prompt result
            self.logging_service.log_prompt_result(
                prompt_type="skills",
                prompt_text=prompt,
                response=message.parsed.dict(),
                messages=messages

            )
            return message.parsed.skills
        else:
            raise ValueError(
                f"Failed to parse skills response: {message.refusal}")

    def _analyze_education(self, cv_text: str, job_title: str):
        prompt = EducationPrompt.format(job_title=job_title)

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": CVPrompt.format(cv_text=cv_text)}
        ]

        completion = self.client.beta.chat.completions.parse(
            model=settings.OPENAI_MODEL,
            messages=messages,
            response_format=EducationResponse,
            seed=settings.OPENAI_SEED,
            temperature=settings.OPENAI_TEMPERATURE
        )

        message = completion.choices[0].message
        if message.parsed:
            # Log prompt result
            self.logging_service.log_prompt_result(
                prompt_type="education",
                prompt_text=prompt,
                response=message.parsed.dict(),
                messages=messages
            )
            return message.parsed.education
        else:
            raise ValueError(
                f"Failed to parse education response: {message.refusal}")

    def _generate_summary(self, cv_text: str, job_title: str,
                          evaluation: CompleteEvaluation,
                          fit_score: float):
        prompt = SummaryPrompt.format(job_title=job_title)
        cv_analysis_text = f"""
            {CVPrompt.format(cv_text=cv_text)}
            
            Análisis previo:
            Experiencias: {evaluation.experiences}
            Habilidades: {evaluation.skills}
            Educación: {evaluation.education}
            Puntuación calculada: {fit_score}
        """

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": cv_analysis_text}
        ]

        completion = self.client.beta.chat.completions.parse(
            model=settings.OPENAI_MODEL,
            messages=messages,
            response_format=SummaryResponse,
            seed=settings.OPENAI_SEED,
            temperature=settings.OPENAI_TEMPERATURE
        )

        message = completion.choices[0].message
        if message.parsed:
            summary = message.parsed.summary
            summary.fit_score = fit_score

            self.logging_service.log_prompt_result(
                prompt_type="summary",
                prompt_text=prompt,
                response=message.parsed.dict(),
                messages=messages
            )

            return summary
        else:
            raise ValueError(
                f"Failed to parse summary response: {message.refusal}")

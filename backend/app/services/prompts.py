from dataclasses import dataclass
import os
from pathlib import Path
from dotenv import load_dotenv
import importlib.util

load_dotenv()

# Load prompts from Python code file at backend root
PROMPT_PY_FILE = Path(__file__).resolve().parents[2] / "System and User Prompt.py"

def _load_prompts_from_python_file():
    system = None
    user = None
    try:
        if PROMPT_PY_FILE.exists():
            spec = importlib.util.spec_from_file_location("cognify_prompts", str(PROMPT_PY_FILE))
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)  # type: ignore
                spec.loader.exec_module(mod)  # type: ignore
                system = getattr(mod, "SYSTEM_PROMPT", None)
                user = getattr(mod, "USER_PROMPT_TEMPLATE", None)
    except Exception:
        pass
    return system, user

@dataclass
class PromptConfig:
    provider: str = os.getenv("PROVIDER", "gemini").lower()
    # Default temperature for sampling (can be overridden per-request)
    temperature: float = float(os.getenv("TEMPERATURE", "0.7"))
    system_prompt: str = os.getenv(
        "SYSTEM_PROMPT",
        "You are an AI tutor that analyzes student answers, detects concept gaps, and suggests targeted learning resources.",
    )
    user_prompt_template: str = os.getenv(
        "USER_PROMPT_TEMPLATE",
        "Given the following quiz answers and context, identify weak concepts and recommend resources. Answers: {answers}. Context: {context}.",
    )
    # Gemini
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    # Ollama
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3")

# Initialize config and override from Python file if present
config = PromptConfig()
file_system, file_user = _load_prompts_from_python_file()
if file_system:
    config.system_prompt = file_system
if file_user:
    config.user_prompt_template = file_user


def render_user_prompt(
    answers: str,
    context: str,
    answer_key: str = "",
    student_profile: str = "",
    constraints: str = "",
) -> str:
    """Render the user prompt template with available placeholders.
    Falls back gracefully if some placeholders are not present in template.
    """
    template = config.user_prompt_template
    try:
        return template.format(
            answers=answers,
            context=context,
            answer_key=answer_key,
            student_profile=student_profile,
            constraints=constraints,
        )
    except KeyError:
        return template.format(answers=answers, context=context)
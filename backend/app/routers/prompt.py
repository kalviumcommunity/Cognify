from fastapi import APIRouter
from pydantic import BaseModel
from ..services.prompts import config, render_user_prompt
from ..services.llm_service import LLMService

router = APIRouter()

class PromptTestRequest(BaseModel):
    answers: str
    context: str = ""
    answer_key: str = ""
    student_profile: str = ""
    constraints: str = ""
    temperature: float | None = None  # Optional per-request override

class PromptTestResponse(BaseModel):
    provider: str
    output: str

@router.post("/prompt-test", response_model=PromptTestResponse)
async def prompt_test(body: PromptTestRequest):
    # Render prompts
    system_prompt = config.system_prompt
    user_prompt = render_user_prompt(
        answers=body.answers,
        context=body.context,
        answer_key=body.answer_key,
        student_profile=body.student_profile,
        constraints=body.constraints,
    )

    # Call provider with optional temperature override
    svc = LLMService()
    result = await svc.generate(system_prompt, user_prompt, temperature=body.temperature)

    if "error" in result:
        return PromptTestResponse(provider=config.provider, output=f"ERROR: {result['error']}")

    return PromptTestResponse(provider=result.get("provider", config.provider), output=result.get("text", ""))
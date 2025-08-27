"""
Zero-Shot Prompting - Code Version
This module exports:
- ZERO_SHOT_SYSTEM_PROMPT: str
- ZERO_SHOT_USER_PROMPT_TEMPLATE: str (format placeholders: {task}, {context}, {input}, {constraints}, {output_schema}, {style})
"""

ZERO_SHOT_SYSTEM_PROMPT = (
    "You are an expert assistant operating in zero-shot mode.\n\n"
    "Principles:\n"
    "- Follow the user's Task and Output requirements exactly.\n"
    "- Base your answer only on the provided Context and Input; do not fabricate facts.\n"
    "- If information is insufficient, state precisely what is missing and proceed with a best-effort answer, clearly marking assumptions.\n"
    "- Prefer concise, unambiguous phrasing appropriate for the audience.\n"
    "- If a structured output schema is provided, match it exactly (field names, types, and order when specified).\n"
    "- Do not include hidden step-by-step reasoning; provide final answers and brief explanations only if required.\n"
    "- Do not invent URLs, citations, or data.\n"
)

ZERO_SHOT_USER_PROMPT_TEMPLATE = (
    "Task:\n"
    "{task}\n\n"
    "Context (optional):\n"
    "{context}\n\n"
    "Input:\n"
    "{input}\n\n"
    "Constraints (optional):\n"
    "{constraints}\n\n"
    "Output requirements / schema (optional):\n"
    "{output_schema}\n\n"
    "Style (optional):\n"
    "{style}\n\n"
    "Instructions:\n"
    "- Produce the final output that satisfies the Task and Output requirements.\n"
    "- If a JSON schema is provided, return only a valid JSON object conforming to it.\n"
    "- If key inputs are missing, list them first under 'missing' and then proceed with the best possible answer.\n"
)
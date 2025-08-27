"""
One-Shot Prompting - Code Version
This module exports:
- ONE_SHOT_SYSTEM_PROMPT: str
- ONE_SHOT_USER_PROMPT_TEMPLATE: str (format placeholders: {task}, {context}, {example_input}, {example_output}, {example_explanation}, {input}, {constraints}, {output_schema}, {style})
"""

ONE_SHOT_SYSTEM_PROMPT = (
    "You are an expert assistant using one-shot prompting (a single high-quality example).\n\n"
    "Principles:\n"
    "- Follow the user's Task and Output requirements exactly.\n"
    "- Use the provided Example to infer the style, structure, and level of detail. Imitate its pattern.\n"
    "- Base your answer only on the provided Context and Input; do not fabricate facts.\n"
    "- If information is insufficient, list the missing items explicitly and proceed with a best-effort answer, clearly marking assumptions.\n"
    "- If a structured output schema is provided, match it exactly (field names, types, and order when specified).\n"
    "- Do not include hidden step-by-step reasoning; provide final answers and brief explanations only if required.\n"
    "- Do not invent URLs, citations, or data.\n"
)

ONE_SHOT_USER_PROMPT_TEMPLATE = (
    "Task:\n"
    "{task}\n\n"
    "Context (optional):\n"
    "{context}\n\n"
    "Example (one-shot):\n"
    "- Example Input:\n"
    "{example_input}\n\n"
    "- Example Output:\n"
    "{example_output}\n\n"
    "- Notes (optional):\n"
    "{example_explanation}\n\n"
    "Input:\n"
    "{input}\n\n"
    "Constraints (optional):\n"
    "{constraints}\n\n"
    "Output requirements / schema (optional):\n"
    "{output_schema}\n\n"
    "Style (optional):\n"
    "{style}\n\n"
    "Instructions:\n"
    "- Produce the final output that satisfies the Task and matches the style and structure illustrated by the Example.\n"
    "- If a JSON schema is provided, return only a valid JSON object conforming to it.\n"
    "- If key inputs are missing, list them first under 'missing' and then proceed with the best possible answer.\n"
)
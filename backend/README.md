# Cognify Backend (FastAPI)

## Setup
1. Create a virtual environment and install deps using pyproject:
   ```bash
   pip install -U pip
   pip install .
   ```
2. Copy .env.example to .env and fill values.
   ```bash
   cp .env.example .env
   ```

## Run
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Test the prompt endpoint
```bash
curl -X POST http://localhost:8000/api/prompt-test \
  -H "Content-Type: application/json" \
  -d '{"answers":"Student chose B for Q1, C for Q2.", "context":"Topic: Algebra - linear equations."}'
```

## Config
- PROVIDER: gemini or ollama
- GEMINI_API_KEY: required for gemini
- OLLAMA_HOST, OLLAMA_MODEL: for ollama
- SYSTEM_PROMPT, USER_PROMPT_TEMPLATE: override defaults
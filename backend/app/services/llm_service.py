import os
import json
from typing import Dict, Any
import httpx
from .prompts import config

# Simple abstraction over providers

class LLMService:
    async def generate(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        provider = config.provider
        if provider == "gemini":
            return await self._call_gemini(system_prompt, user_prompt)
        elif provider == "ollama":
            return await self._call_ollama(system_prompt, user_prompt)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    async def _call_gemini(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        api_key = config.gemini_api_key
        if not api_key:
            return {"error": "Missing GEMINI_API_KEY"}
        # Gemini Generative Language API (v1beta) - text responses
        # Endpoint can vary; using contents:generate via REST
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {"role": "user", "parts": [{"text": f"System: {system_prompt}\nUser: {user_prompt}"}]}
            ]
        }
        params = {"key": api_key}
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(url, headers=headers, params=params, json=payload)
            data = resp.json()
            if resp.status_code >= 400:
                return {"error": data}
            # Extract text
            try:
                text = data["candidates"][0]["content"]["parts"][0]["text"]
            except Exception:
                text = json.dumps(data)
            return {"provider": "gemini", "text": text, "raw": data}

    async def _call_ollama(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        url = f"{config.ollama_host}/api/generate"
        payload = {
            "model": config.ollama_model,
            "prompt": user_prompt,
            "system": system_prompt,
            "stream": False,
        }
        async with httpx.AsyncClient(timeout=120) as client:
            resp = await client.post(url, json=payload)
            data = resp.json()
            if resp.status_code >= 400:
                return {"error": data}
            text = data.get("response", "")
            return {"provider": "ollama", "text": text, "raw": data}
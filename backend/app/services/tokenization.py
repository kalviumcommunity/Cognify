"""
Tokenization utilities for Cognify backend.

Features (no extra dependencies):
- Word and sentence tokenization via regex
- Character/word counts
- Heuristic LLM token estimation (approximation)
- Helpers to estimate prompt token usage

Notes:
- Exact tokenization differs by provider/model. This module provides
  a reasonable approximation and a pluggable interface to add
  provider-specific implementations later without breaking callers.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
import re
from typing import Dict, List, Optional

# Regex patterns for lightweight tokenization
WORD_RE = re.compile(r"\b\w+\b", re.UNICODE)
# Split on end-of-sentence punctuation followed by whitespace and a new sentence start
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")

# Average chars per token heuristic.
# Common guideline: ~4 chars/token for English text, ~1.5 words/token.
DEFAULT_CHARS_PER_TOKEN = 4.0


# -----------------------------
# Basic tokenization primitives
# -----------------------------

def tokenize_words(text: str) -> List[str]:
    """Return a list of word-like tokens using a simple regex.
    This is language-agnostic and may not handle all scripts perfectly.
    """
    if not text:
        return []
    return WORD_RE.findall(text)


def tokenize_sentences(text: str) -> List[str]:
    """Split text into sentences using a simple regex heuristic.
    Falls back gracefully if input is empty.
    """
    if not text:
        return []
    text = text.strip()
    if not text:
        return []
    parts = SENTENCE_SPLIT_RE.split(text)
    # Ensure we don't return empty fragments
    return [p.strip() for p in parts if p.strip()]


def count_chars(text: str) -> int:
    return len(text or "")


def count_words(text: str) -> int:
    return len(tokenize_words(text))


# ---------------------------------
# LLM-focused token count estimation
# ---------------------------------
@dataclass
class TokenEstimationOptions:
    provider: str = "generic"  # e.g., "gemini", "ollama"
    model: Optional[str] = None # e.g., "llama3"
    chars_per_token: Optional[float] = None  # override heuristic if known


def estimate_llm_tokens(text: str, options: Optional[TokenEstimationOptions] = None) -> int:
    """Estimate the number of LLM tokens for the given text.

    This uses a simple chars-per-token heuristic. For most English text,
    tokens ≈ ceil(len(text) / 4). You can override via options.chars_per_token.

    For exact counts, integrate the provider/model tokenizer later.
    """
    if not text:
        return 0

    if options is None:
        options = TokenEstimationOptions()

    # Allow provider/model-specific overrides here if you know exact ratios.
    cpt = options.chars_per_token

    if cpt is None:
        provider = (options.provider or "generic").lower()
        model = (options.model or "").lower()

        # Placeholder for future specialization
        # Example heuristics if desired:
        # - Gemini: keep default
        # - LLaMA-family: slightly fewer chars per token on average
        if provider == "ollama" and ("llama" in model or "llama" in provider):
            cpt = 3.6
        else:
            cpt = DEFAULT_CHARS_PER_TOKEN

    return int(math.ceil(len(text) / max(cpt, 0.1)))


def estimate_prompt_tokens(
    system_prompt: str,
    user_prompt: str,
    options: Optional[TokenEstimationOptions] = None,
) -> Dict[str, int]:
    """Estimate token usage for a prompt pair.

    Returns a dict with per-part and total estimates.
    """
    sys_tokens = estimate_llm_tokens(system_prompt, options)
    user_tokens = estimate_llm_tokens(user_prompt, options)
    return {
        "system": sys_tokens,
        "user": user_tokens,
        "total": sys_tokens + user_tokens,
    }


# ---------------------------------
# Utilities for fitting within limits
# ---------------------------------

def split_text_to_fit_tokens(
    text: str,
    max_tokens: int,
    options: Optional[TokenEstimationOptions] = None,
) -> str:
    """Return a prefix of text that fits within the estimated token budget.

    Strategy:
    1) Estimate chars-per-token to compute an approximate char budget.
    2) Try to cut on sentence boundary within that budget.
    3) Fallback to a hard char cut if needed.
    """
    if not text or max_tokens <= 0:
        return ""

    if options is None:
        options = TokenEstimationOptions()

    # Convert token budget to char budget
    cpt = options.chars_per_token or (
        3.6 if ((options.provider or "").lower() == "ollama" and (options.model or "").lower().startswith("llama")) else DEFAULT_CHARS_PER_TOKEN
    )
    char_budget = max(1, int(max_tokens * cpt))

    if len(text) <= char_budget:
        return text

    # Try sentence-aware truncation
    sentences = tokenize_sentences(text)
    out: List[str] = []
    running = 0
    for s in sentences:
        # +1 for the space/newline joiner when reconstructed
        delta = len(s) + (1 if out else 0)
        if running + delta > char_budget:
            break
        out.append(s)
        running += delta

    if out:
        return (" ".join(out)).strip()

    # Fallback hard cut
    return text[:char_budget].rstrip()


# -----------------------------
# Example usage (documentation)
# -----------------------------
# from app.services.tokenization import (
#     tokenize_words, tokenize_sentences, count_chars, count_words,
#     estimate_llm_tokens, estimate_prompt_tokens, TokenEstimationOptions,
# )
#
# text = "Hello world! This is a test."
# words = tokenize_words(text)                 # ["Hello", "world", "This", ...]
# sentences = tokenize_sentences(text)         # ["Hello world!", "This is a test."]
# char_count = count_chars(text)               # e.g., 29
# word_count = count_words(text)               # e.g., 6
# tokens = estimate_llm_tokens(text)           # heuristic token estimate
# prompt_tokens = estimate_prompt_tokens("System", "User message")
#
# To specialize for Ollama LLaMA3:
# opts = TokenEstimationOptions(provider="ollama", model="llama3")
# tokens_llama = estimate_llm_tokens(text, opts)
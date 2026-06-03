"""
GovAgent — Centralised LLM Factory
=====================================
Provides a single ``get_llm()`` function that returns a configured
Groq-backed ChatModel.

Usage::

    from src.llm import get_llm
    llm = get_llm()
    response = llm.invoke("Hello!")
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_ENV_PATH)


# ---------------------------------------------------------------------------
# LLM factory
# ---------------------------------------------------------------------------

def get_llm(temperature: float = 0.3, model: str | None = None,
            trace_name: str | None = None):
    """Return a configured ChatGroq instance.

    Parameters
    ----------
    temperature : float
        Sampling temperature (0 = deterministic, 1 = creative).
    model : str | None
        Groq model name.  Defaults to ``GROQ_MODEL`` env var or
        ``llama-3.3-70b-versatile``.
    trace_name : str | None
        Reserved for future use. Currently ignored.

    Returns
    -------
    ChatGroq
        A ready-to-use LangChain chat model.

    Raises
    ------
    ValueError
        If ``GROQ_API_KEY`` is not set or is still the placeholder.
    """
    from langchain_groq import ChatGroq

    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key or api_key.startswith("your-"):
        raise ValueError(
            "GROQ_API_KEY is not set.  Please add your key to the .env file.\n"
            "Get one at: https://console.groq.com/keys"
        )

    model_name = model or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    return ChatGroq(
        api_key=api_key,
        model=model_name,
        temperature=temperature,
        max_tokens=4096,
    )

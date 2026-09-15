import os
import json
import logging
from typing import Optional, Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from backend.app.config import settings

logger = logging.getLogger("travel_planner.llm")

def get_llm():
    """
    Get the configured Groq LLM instance or None if key is not configured.
    """
    api_key = settings.GROQ_API_KEY or os.environ.get("GROQ_API_KEY", "")
    if api_key and api_key.strip() and api_key != "your_groq_api_key_here":
        try:
            from langchain_groq import ChatGroq
            return ChatGroq(
                groq_api_key=api_key,
                model_name=settings.GROQ_MODEL,
                temperature=0.4,
                max_tokens=4096
            )
        except Exception as e:
            logger.warning(f"Failed to initialize ChatGroq: {e}. Falling back to smart generator.")
            return None
    return None

def invoke_llm_json(prompt: str, system_prompt: str) -> Optional[Dict[str, Any]]:
    """
    Invoke LLM and parse JSON response.
    """
    llm = get_llm()
    if not llm:
        return None
    try:
        messages = [
            SystemMessage(content=system_prompt + "\nYou MUST return only valid, parseable JSON matching the requested structure without markdown fences or extra chatter."),
            HumanMessage(content=prompt)
        ]
        response = llm.invoke(messages)
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        return json.loads(content.strip())
    except Exception as e:
        logger.error(f"Error invoking Groq LLM: {e}")
        return None

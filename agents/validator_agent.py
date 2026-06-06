import json
import logging
import re

from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)

llm = ChatOpenAI(
    model="gpt-4o-mini"
)


def _extract_json_from_text(text: str):
    """Try to extract a JSON object from text using a simple brace matcher."""
    if not text:
        return None
    # first try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # attempt to find the first {...} block
    m = re.search(r"\{.*\}", text, re.S)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            return None

    return None


def validator_agent(state):

    prompt = f"""
Review classification.

Classification:
{state["category"]}

Reason:
{state["reasoning"]}

Evidence:
{state["evidence"]}

Return JSON:

{{
    "agree": true,
    "reason": ""
}}
"""

    response = llm.invoke(prompt)

    # Normalize possible response shapes to a string
    raw = None
    if hasattr(response, "content"):
        raw = response.content
    elif hasattr(response, "text"):
        raw = response.text
    else:
        try:
            raw = json.dumps(response)
        except Exception:
            raw = str(response)

    if isinstance(raw, (bytes, bytearray)):
        try:
            raw = raw.decode()
        except Exception:
            raw = raw.decode(errors="ignore")

    result = _extract_json_from_text(raw)

    if result is None:
        logger.warning("Validator received non-JSON response: %s", raw)
        # Fallback: mark as disagreement and store raw text as reason
        result = {"agree": False, "reason": f"Unparseable response: {raw}"}

    state["validator_agreement"] = result.get("agree", False)
    state["validator_reason"] = result.get("reason", "")

    return state
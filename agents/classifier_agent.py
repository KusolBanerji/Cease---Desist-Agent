import json
import logging
import re

from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)

llm = ChatOpenAI(
    model="gpt-4.1"
)


def _extract_json_from_text(text: str):
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    m = re.search(r"\{.*\}", text, re.S)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            return None

    return None


def classifier_agent(state):

    text = state.get("translated_text", "") or ""

    prompt = f"""
Classify this customer document.

Possible categories:

1. CEASE
2. UNCERTAIN
3. IRRELEVANT

Return JSON:

{{
    "category":"",
    "confidence":0.0,
    "evidence":[],
    "reasoning":""
}}

Document:

{text}
"""

    response = llm.invoke(prompt)

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
        logger.warning("Classifier received non-JSON response: %s", raw)
        result = {
            "category": "UNCERTAIN",
            "confidence": 0.0,
            "evidence": [],
            "reasoning": f"Unparseable response: {raw}"
        }

    state["category"] = result.get("category", "UNCERTAIN")
    state["confidence"] = result.get("confidence", 0.0)
    state["evidence"] = result.get("evidence", [])
    state["reasoning"] = result.get("reasoning", "")

    return state
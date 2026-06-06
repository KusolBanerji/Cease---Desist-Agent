from langdetect import detect
import logging

logger = logging.getLogger(__name__)


def language_agent(state):

    text = state.get("extracted_text", "") or ""

    if not text.strip():
        logger.warning("No text available for language detection. Falling back to 'unknown'.")
        state["language"] = "unknown"
        state["translated_text"] = ""
        return state

    try:
        language = detect(text)
    except Exception as exc:
        logger.warning("Language detection failed: %s", exc)
        language = "unknown"

    state["language"] = language

    state["translated_text"] = text

    return state
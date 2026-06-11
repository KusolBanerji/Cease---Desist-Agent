from langchain_openai import ChatOpenAI
import json

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


def desist_agent(state):

    text = state["translated_text"]

    prompt = f"""
    You are a DESIST classification expert.

    Analyze the document.

    Return ONLY valid JSON.

    Schema:

    {{
        "confidence": 0.0,
        "reasoning": "",
        "evidence": []
    }}

    Rules:
    - confidence between 0 and 1
    - evidence must be list
    - no markdown
    - no explanations
    - raw JSON only

    Document:

    {text}
    """

    response = llm.invoke(prompt)

    content = response.content.strip()

    try:

        result = json.loads(content)

    except Exception as e:

        print(
            f"[DESIST AGENT] JSON parse error: {e}"
        )

        result = {
            "confidence": 0.0,
            "reasoning":
                "JSON parsing failed",
            "evidence": []
        }

    state["desist_confidence"] = (
        result["confidence"]
    )

    print(
        f"[DESIST AGENT] "
        f"{state['desist_confidence']}"
    )

    return state
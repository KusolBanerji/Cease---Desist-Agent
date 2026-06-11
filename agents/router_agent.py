from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


def router_agent(state):

    text = state["translated_text"]

    prompt = f"""
    Classify the document into one candidate:

    CEASE
    DESIST
    IRRELEVANT

    Return only one word.

    Document:
    {text}
    """

    response = llm.invoke(prompt)

    state["candidate_type"] = (
        response.content.strip().upper()
    )

    print(
        f"[ROUTER] Candidate: "
        f"{state['candidate_type']}"
    )

    return state
import uuid


def intake_agent(state):

    state["document_id"] = str(uuid.uuid4())

    return state
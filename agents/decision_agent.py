from config import CONFIDENCE_THRESHOLD


def decision_agent(state):

    cease_score = state["cease_confidence"]

    desist_score = state["desist_confidence"]

    print(f"CEASE={state['cease_confidence']}")

    print(f"DESIST={state['desist_confidence']}")

    if max(
        cease_score,
        desist_score
    ) < CONFIDENCE_THRESHOLD:

        state["category"] = "HUMAN_REVIEW"

    elif cease_score >= desist_score:

        state["category"] = "CEASE"

    else:

        state["category"] = "DESIST"

    return state
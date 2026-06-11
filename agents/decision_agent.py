from config import (
    CONFIDENCE_THRESHOLD
)


def decision_agent(state):

    cease_score = (
        state["cease_confidence"]
    )

    desist_score = (
        state["desist_confidence"]
    )

    if (
        cease_score >= CONFIDENCE_THRESHOLD
        and
        cease_score > desist_score
    ):

        state["category"] = "CEASE"

    elif (
        desist_score >= CONFIDENCE_THRESHOLD
        and
        desist_score > cease_score
    ):

        state["category"] = "DESIST"

    else:

        state["category"] = (
            "HUMAN_REVIEW"
        )

    print(
        f"[DECISION] "
        f"{state['category']}"
    )

    return state
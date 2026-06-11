from db.database import SessionLocal
from db.models import CeaseRequest


def cease_persistence_agent(state):

    db = SessionLocal()

    try:

        state["final_decision"] = (
            state["category"]
        )

        confidence = max(
            state.get(
                "cease_confidence",
                0.0
            ),
            state.get(
                "desist_confidence",
                0.0
            )
        )

        record = CeaseRequest(
            document_id=state["document_id"],
            filename=state["filename"],
            category=state["category"],
            confidence=confidence
        )

        db.add(record)

        db.commit()

        print(
            f"[PERSISTENCE] Saved "
            f"{state['category']} "
            f"for {state['filename']}"
        )

    except Exception as e:

        print(
            f"[PERSISTENCE ERROR] {e}"
        )

    finally:

        db.close()

    return state
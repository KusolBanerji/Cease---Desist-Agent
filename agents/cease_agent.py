from db.database import SessionLocal
from db.models import CeaseRequest


def cease_agent(state):

    state["final_decision"] = "CEASE"

    db = SessionLocal()

    try:

        record = CeaseRequest(
            document_id=state["document_id"],
            filename=state["filename"],
            category=state["final_decision"],
            confidence=state["confidence"]
        )

        db.add(record)
        db.commit()

        print(
            f"[CEASE AGENT] Saved {state['document_id']}"
        )

    except Exception as e:

        print(
            f"[CEASE AGENT ERROR] {e}"
        )

        db.rollback()

    finally:

        db.close()

    return state
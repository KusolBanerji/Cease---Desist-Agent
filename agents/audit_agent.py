import json

from db.database import SessionLocal
from db.models import AuditLog


def audit_agent(state):

    db = SessionLocal()

    try:

        record = AuditLog(
            document_id=state["document_id"],
            filename=state["filename"],
            category=state["category"],
            confidence=state["confidence"],
            reasoning=state["reasoning"],
            evidence=json.dumps(
                state["evidence"]
            ),

            validator_agreement=str(
                state["validator_agreement"]
            ),

            validator_reason=state[
                "validator_reason"
            ],

            final_decision=state[
                "final_decision"
            ]
        )

        db.add(record)

        db.commit()

        print(
            f"[AUDIT AGENT] Logged {state['document_id']}"
        )

    except Exception as e:

        print(
            f"[AUDIT AGENT ERROR] {e}"
        )

        db.rollback()

    finally:

        db.close()

    return state
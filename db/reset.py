import os

from db.database import SessionLocal
from db.models import (
    CeaseRequest,
    AuditLog,
    HumanReviewQueue
)


def reset_database():

    db = SessionLocal()

    try:

        db.query(
            CeaseRequest
        ).delete()

        db.query(
            AuditLog
        ).delete()

        db.query(
            HumanReviewQueue
        ).delete()

        db.commit()

        print(
            "[RESET] Database cleared"
        )

    finally:

        db.close()
from db.database import SessionLocal
from db.models import (
    CeaseRequest,
    AuditLog,
    HumanReviewQueue
)


def get_cease_count():

    db = SessionLocal()

    count = db.query(
        CeaseRequest
    ).count()

    db.close()

    return count


def get_audit_count():

    db = SessionLocal()

    count = db.query(
        AuditLog
    ).count()

    db.close()

    return count


def get_pending_reviews():

    db = SessionLocal()

    count = db.query(
        HumanReviewQueue
    ).filter(
        HumanReviewQueue.status == "PENDING"
    ).count()

    db.close()

    return count

def get_review_queue():

    db = SessionLocal()

    records = db.query(
        HumanReviewQueue
    ).filter(
        HumanReviewQueue.status == "PENDING"
    ).all()

    db.close()

    return records

def update_review_decision(
        review_id,
        reviewer_name,
        decision
):

    db = SessionLocal()

    record = db.query(
        HumanReviewQueue
    ).filter(
        HumanReviewQueue.id == review_id
    ).first()

    if record:

        record.status = "COMPLETED"

        record.reviewer_name = (
            reviewer_name
        )

        record.final_decision = (
            decision
        )

        db.commit()

    db.close()
from db.database import SessionLocal
from db.models import HumanReviewQueue


def add_to_review_queue(
        document_id,
        filename,
        category,
        confidence,
        reasoning
):

    db = SessionLocal()

    try:

        record = HumanReviewQueue(
            document_id=document_id,
            filename=filename,
            predicted_category=category,
            confidence=confidence,
            reasoning=reasoning,
            status="PENDING"
        )

        db.add(record)

        db.commit()

    finally:

        db.close()
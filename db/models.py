from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Integer

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CeaseRequest(Base):
    __tablename__ = "cease_requests"
    id = Column(Integer, primary_key=True)
    document_id = Column(String)
    filename = Column(String)
    category = Column(String)
    confidence = Column(Float)


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    document_id = Column(String)
    filename = Column(String)
    category = Column(String)
    confidence = Column(Float)
    reasoning = Column(String)
    evidence = Column(String)
    validator_agreement = Column(String)
    validator_reason = Column(String)
    final_decision = Column(String)

class HumanReviewQueue(Base):
    __tablename__ = "human_review_queue"
    id = Column(
        Integer,
        primary_key=True
    )
    document_id = Column(String)
    filename = Column(String)
    predicted_category = Column(String)
    confidence = Column(Float)
    reasoning = Column(String)
    status = Column(
        String,
        default="PENDING"
    )
    reviewer_name = Column(String)
    final_decision = Column(String)
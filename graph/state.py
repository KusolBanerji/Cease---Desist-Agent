from typing import TypedDict, List

class WorkflowState(TypedDict):
    document_id: str
    filename: str
    file_path: str
    extracted_text: str
    language: str
    translated_text: str
    candidate_type: str
    category: str
    confidence: float
    cease_confidence: float
    desist_confidence: float
    evidence: List[str]
    reasoning: str
    validator_agreement: bool
    validator_reason: str
    final_decision: str
    requires_human_review: bool
    review_status: str
    human_decision: str
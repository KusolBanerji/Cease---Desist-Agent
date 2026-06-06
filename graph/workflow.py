from langgraph.graph import StateGraph
from langgraph.graph import END

from graph.state import WorkflowState

from config import CONFIDENCE_THRESHOLD

from db.review_queue import add_to_review_queue

from agents.intake_agent import intake_agent
from agents.ocr_agent import ocr_agent
from agents.language_agent import language_agent
from agents.classifier_agent import classifier_agent
from agents.validator_agent import validator_agent
from agents.cease_agent import cease_agent
from agents.archive_agent import archive_agent
from agents.audit_agent import audit_agent

def route_document(state):
    confidence = state["confidence"]
    category = state["category"]
    validator_agreement = state["validator_agreement"]

    if not validator_agreement:
        return "human_review"

    if confidence < CONFIDENCE_THRESHOLD:
        return "human_review"

    if category == "CEASE":
        return "cease"

    if category == "IRRELEVANT":
        return "archive"

    return "human_review"

def human_review_node(state):

    add_to_review_queue(
        document_id=state["document_id"],
        filename=state["filename"],
        category=state["category"],
        confidence=state["confidence"],
        reasoning=state["reasoning"]
    )

    state["requires_human_review"] = True
    state["review_status"] = "PENDING"
    state["final_decision"] = "HUMAN_REVIEW"

    print(f"[HUMAN REVIEW] {state['filename']}")

    return state

def build_graph():

    workflow = StateGraph(
        WorkflowState
    )

    workflow.add_node(
        "intake",
        intake_agent
    )

    workflow.add_node(
        "ocr",
        ocr_agent
    )

    workflow.add_node(
        "language",
        language_agent
    )

    workflow.add_node(
        "classifier",
        classifier_agent
    )

    workflow.add_node(
        "validator",
        validator_agent
    )

    workflow.add_node(
        "cease",
        cease_agent
    )

    workflow.add_node(
        "archive",
        archive_agent
    )

    workflow.add_node(
        "human_review",
        human_review_node
    )

    workflow.add_node(
        "audit",
        audit_agent
    )

    workflow.set_entry_point(
        "intake"
    )

    workflow.add_edge(
        "intake",
        "ocr"
    )

    workflow.add_edge(
        "ocr",
        "language"
    )

    workflow.add_edge(
        "language",
        "classifier"
    )

    workflow.add_edge(
        "classifier",
        "validator"
    )

    workflow.add_conditional_edges(
        "validator",
        route_document,
        {
            "cease": "cease",
            "archive": "archive",
            "human_review": "human_review"
        }
    )

    workflow.add_edge(
        "cease",
        "audit"
    )

    workflow.add_edge(
        "archive",
        "audit"
    )

    workflow.add_edge(
        "human_review",
        "audit"
    )

    workflow.add_edge(
        "audit",
        END
    )

    return workflow.compile()

graph = build_graph()
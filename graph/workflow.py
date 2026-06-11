from langgraph.graph import StateGraph
from langgraph.graph import END

from graph.state import WorkflowState

from config import CONFIDENCE_THRESHOLD

from db.review_queue import add_to_review_queue

from agents.intake_agent import intake_agent
from agents.ocr_agent import ocr_agent
from agents.language_agent import language_agent

from agents.router_agent import router_agent

from agents.cease_agent import cease_agent
from agents.desist_agent import desist_agent

from agents.decision_agent import decision_agent

from agents.cease_persistence_agent import cease_persistence_agent

from agents.archive_agent import archive_agent
from agents.audit_agent import audit_agent


# --------------------------------------------------
# HUMAN REVIEW NODE
# --------------------------------------------------

def human_review_node(state):

    add_to_review_queue(
        document_id=state["document_id"],
        filename=state["filename"],
        category=state["category"],
        confidence=max(
            state["cease_confidence"],
            state["desist_confidence"]
        ),
        reasoning=state["reasoning"]
    )

    state["requires_human_review"] = True

    state["review_status"] = "PENDING"

    state["final_decision"] = "HUMAN_REVIEW"

    print(
        f"[HUMAN REVIEW] "
        f"{state['filename']}"
    )

    return state


# --------------------------------------------------
# ROUTING LOGIC
# --------------------------------------------------

def route_document(state):

    category = state["category"]

    if category == "CEASE":

        return "cease_final"

    elif category == "DESIST":

        return "cease_final"

    elif category == "IRRELEVANT":

        return "archive"

    else:

        return "human_review"


# --------------------------------------------------
# BUILD GRAPH
# --------------------------------------------------

def build_graph():

    workflow = StateGraph(
        WorkflowState
    )

    # ---------------------------
    # Nodes
    # ---------------------------

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
        "router",
        router_agent
    )

    workflow.add_node(
        "cease",
        cease_agent
    )

    workflow.add_node(
        "desist",
        desist_agent
    )

    workflow.add_node(
        "decision",
        decision_agent
    )

    workflow.add_node(
        "cease_final",
        cease_persistence_agent
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

    # ---------------------------
    # Entry Point
    # ---------------------------

    workflow.set_entry_point(
        "intake"
    )

    # ---------------------------
    # Main Flow
    # ---------------------------

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
        "router"
    )

    workflow.add_edge(
        "router",
        "cease"
    )

    workflow.add_edge(
        "cease",
        "desist"
    )

    workflow.add_edge(
        "desist",
        "decision"
    )

    # ---------------------------
    # Conditional Routing
    # ---------------------------

    workflow.add_conditional_edges(
        "decision",
        route_document,
        {
            "cease_final": "cease_final",
            "archive": "archive",
            "human_review": "human_review"
        }
    )

    # ---------------------------
    # Final Steps
    # ---------------------------

    workflow.add_edge(
        "cease_final",
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
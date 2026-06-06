from agents.cease_agent import cease_agent
from agents.archive_agent import archive_agent
from agents.audit_agent import audit_agent


state = {

    "document_id": "DOC001",

    "filename": "sample.pdf",

    "category": "CEASE",

    "confidence": 0.95,

    "reasoning": "Customer requested all communication stop.",

    "evidence": [
        "stop contacting me",
        "cease all communication"
    ],

    "validator_agreement": True,

    "validator_reason": "Evidence supports decision",

    "final_decision": "IRRELEVANT"
}


#cease_agent(state)

#audit_agent(state)

archive_agent(state)
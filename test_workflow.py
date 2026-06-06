from graph.workflow import graph


state = {

    "filename": "sample.pdf",

    "file_path": "input_pdfs/sample.pdf",

    "document_id": "",

    "extracted_text": "",

    "language": "",

    "translated_text": "",

    "category": "",

    "confidence": 0.0,

    "evidence": [],

    "reasoning": "",

    "validator_agreement": False,

    "validator_reason": "",

    "final_decision": "",

    "requires_human_review": False,

    "review_status": "",

    "human_decision": ""
}


result = graph.invoke(state)

print(result)
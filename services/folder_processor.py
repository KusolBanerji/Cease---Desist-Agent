import os

from graph.workflow import graph


def process_folder(folder_path="input_pdfs"):

    results = []

    pdf_files = [
        file
        for file in os.listdir(folder_path)
        if file.lower().endswith(".pdf")
    ]

    for pdf_file in pdf_files:

        file_path = os.path.join(
            folder_path,
            pdf_file
        )

        print(
            f"\nProcessing: {pdf_file}"
        )

        state = {

            "document_id": "",

            "filename": pdf_file,

            "file_path": file_path,

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

        results.append(result)

    return results
import fitz


def ocr_agent(state):

    pdf_path = state["file_path"]

    text = ""

    doc = fitz.open(pdf_path)

    for page in doc:

        text += page.get_text()

    state["extracted_text"] = text

    return state
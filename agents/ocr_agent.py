import fitz
import pytesseract

from pdf2image import convert_from_path
from pdf2image.exceptions import PDFInfoNotInstalledError

from config import TESSERACT_PATH, POPPLER_PATH

pytesseract.pytesseract.tesseract_cmd = (
    TESSERACT_PATH
)


def ocr_agent(state):

    pdf_path = state["file_path"]

    text = ""

    # --------------------------------
    # Try Native PDF Extraction
    # --------------------------------

    doc = fitz.open(pdf_path)

    for page in doc:

        text += page.get_text()

    # --------------------------------
    # Fallback OCR
    # --------------------------------

    if not text.strip():

        print(
            "[OCR] No text layer found. "
            "Running OCR..."
        )

        convert_kwargs = {}
        if POPPLER_PATH:
            convert_kwargs["poppler_path"] = POPPLER_PATH
            print(f"[OCR] Using Poppler path: {POPPLER_PATH}")

        try:
            images = convert_from_path(pdf_path, **convert_kwargs)
        except PDFInfoNotInstalledError as exc:
            raise RuntimeError(
                "[OCR] Poppler is not installed or not available on PATH. "
                "Set POPPLER_PATH to the folder containing pdfinfo.exe, or add it to PATH."
            ) from exc
        except Exception as exc:
            raise RuntimeError(
                "[OCR] Failed to convert PDF to images with Poppler. "
                "Verify Poppler is installed and POPPLER_PATH is correct."
            ) from exc

        for image in images:

            text += pytesseract.image_to_string(
                image
            )

    state["extracted_text"] = text

    print(
        f"[OCR] Extracted "
        f"{len(text)} characters"
    )

    return state
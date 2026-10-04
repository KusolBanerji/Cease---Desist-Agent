# Cease & Desist Agent

An agentic AI workflow for reviewing incoming PDF documents and identifying whether they are likely cease-and-desist notices, desist letters, irrelevant documents, or items requiring human review.

This project combines OCR, language detection, and multiple LLM-based classification agents into a LangGraph workflow. It is designed to process a folder of PDF files, extract their text, classify them, log decisions, and surface uncertain cases to a human reviewer.

## What the project does

The system is intended to handle the following workflow:

1. Intake a PDF document
2. Extract text using PDF parsing and OCR fallback
3. Detect the language of the extracted text
4. Route the document through a decision pipeline
5. Evaluate the document as likely:
   - CEASE
   - DESIST
   - IRRELEVANT
   - HUMAN_REVIEW
6. Persist results in SQLite and show them in a Streamlit dashboard
7. Allow human reviewers to approve or override uncertain classifications

## Core features

- PDF text extraction with fallback OCR
- Multi-agent classification workflow using LangGraph
- CEASE and DESIST scoring agents
- Confidence threshold gating for uncertain cases
- Human review queue for ambiguous documents
- SQLite-backed persistence for processed documents and audit logs
- Streamlit dashboard for monitoring processed files and pending reviews
- Archive logging for irrelevant documents

## Project architecture

The repo uses a small multi-agent pipeline built with LangGraph:

- `agents/intake_agent.py` creates a document ID
- `agents/ocr_agent.py` extracts text from PDFs and falls back to OCR when needed
- `agents/language_agent.py` detects and preserves the document language
- `agents/router_agent.py` makes an initial CEASE/DESIST/IRRELEVANT candidate classification
- `agents/cease_agent.py` evaluates the likelihood of a cease letter
- `agents/desist_agent.py` evaluates the likelihood of a desist letter
- `agents/decision_agent.py` decides between CEASE, DESIST, or human review using a confidence threshold
- `agents/archive_agent.py` logs obviously irrelevant files
- `agents/cease_persistence_agent.py` saves accepted decisions to the database
- `agents/audit_agent.py` writes audit records for each processing run
- `graph/workflow.py` composes the pipeline into a LangGraph state machine

## Repository structure

```text
.
├── README.md
├── requirements.txt
├── config.py
├── app.py
├── cease_desist.db
├── input_pdfs/                  # sample PDFs for processing
├── archive/                     # archive log output
├── agents/                      # classification and processing agents
├── app/                         # Streamlit dashboard and review pages
├── db/                          # SQLite models, reset, and query code
├── graph/                       # LangGraph workflow state and orchestration
├── services/                    # startup and reset utilities
├── __pycache__/                 # compiled Python cache files
├── Capstone_Guidelines.docx     # project guidance document
├── Readme.pdf                  # PDF version of project documentation
└── .gitignore
```

## Tech stack

- Python
- LangGraph
- LangChain / LangChain OpenAI
- OpenAI GPT models
- Streamlit
- SQLite / SQLAlchemy
- PyMuPDF (`fitz`)
- OCR via Tesseract and `pdf2image`
- `langdetect`

## Setup and installation

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# or .venv\Scripts\activate  # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root with your OpenAI key:

```dotenv
OPENAI_API_KEY=your_openai_api_key_here
POPPLER_PATH=C:/path/to/poppler/bin
```

### 4. Install external dependencies

This project expects:

- Tesseract OCR installed and available on PATH or configured via `config.py`
- Poppler installed for PDF-to-image conversion if OCR fallback is needed

On Windows, the default Tesseract path is configured in `config.py` as:

```python
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

If your installation path differs, update it before running the workflow.

## Running the application

### Initialize the database

```bash
python app.py
```

This creates the SQLite database used by the project.

### Start the dashboard

```bash
streamlit run app/streamlit_app.py
```

The Streamlit app:

- displays counts for cease requests, audited docs, and pending review items
- lets you process all PDFs in `input_pdfs/`
- shows the results of the routing and classification workflow

### Human review page

The repository includes a second page at:

```text
app/pages/1_Human_Review.py
```

This page pulls pending review items from the database and lets reviewers approve a document as:

- CEASE
- DESIST
- IRRELEVANT

## Data flow

The typical document flow looks like this:

```text
PDF file
  -> OCR extraction
  -> language detection
  -> candidate routing
  -> cease agent + desist agent
  -> decision agent
  -> archive or persist result
  -> audit log and review queue
```

## Database model

The project stores classification outcomes in SQLite using SQLAlchemy models defined in `db/models.py`:

- `CeaseRequest`
  - stores processed document ID, filename, category, confidence
- `AuditLog`
  - stores reasoning, evidence, validator agreement, and final decision
- `HumanReviewQueue`
  - stores pending human-review tasks

## Example usage

Place PDF documents in the `input_pdfs/` folder and run the app. The workflow will process each file and return a decision based on extracted text and model confidence.

If the document is too ambiguous or below the configured threshold, it is sent to human review instead of being auto-classified.

## Notes

- This is a prototype/experimental workflow, not a production legal-review system.
- Classification quality depends heavily on the quality of the PDF text extraction and the OpenAI model being used.
- The code includes a strong human-in-the-loop review step for uncertain or borderline cases.

## License

No explicit license file is included in this repository, so the project should be treated as unlicensed unless a license is added later.

## Maintainer

This repository appears to be a student or prototype project focused on automating cease-and-desist document triage with AI.

---

If you want, I can also generate a more polished version of this README tailored for GitHub with badges, screenshots, architecture diagrams, and a stronger project pitch.

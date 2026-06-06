import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st

from services.startup import (
    initialize_application
)

from services.folder_processor import (
    process_folder
)

from db.queries import (
    get_cease_count,
    get_audit_count,
    get_pending_reviews
)

if "initialized" not in st.session_state:

    initialize_application()

    st.session_state.initialized = True

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Cease & Desist Agent",
    layout="wide"
)

st.title(
    "Cease & Desist Agentic AI"
)

# --------------------------------------------------
# DASHBOARD METRICS
# (STEP 4)
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Cease Requests",
        get_cease_count()
    )

with col2:

    st.metric(
        "Documents Audited",
        get_audit_count()
    )

with col3:

    st.metric(
        "Pending Reviews",
        get_pending_reviews()
    )

# --------------------------------------------------
# DOCUMENT PROCESSING
# (STEP 5)
# --------------------------------------------------

st.divider()

st.subheader(
    "Document Processing"
)

# --------------------------------------------------
# SESSION STATE
# (STEP 6)
# --------------------------------------------------

if "results" not in st.session_state:

    st.session_state.results = []

# --------------------------------------------------
# PROCESS BUTTON
# (STEP 6)
# --------------------------------------------------

if st.button(
    "Process PDF Folder"
):

    with st.spinner(
        "Processing documents..."
    ):

        st.session_state.results = (
            process_folder()
        )

    st.success(
        f"{len(st.session_state.results)} PDFs processed"
    )

# --------------------------------------------------
# RESULTS DISPLAY
# (STEP 6)
# --------------------------------------------------

if st.session_state.results:

    st.subheader(
        "Processing Results"
    )

    for result in st.session_state.results:

        st.write(
            {
                "Filename":
                    result["filename"],

                "Decision":
                    result["final_decision"],

                "Confidence":
                    result["confidence"]
            }
        )
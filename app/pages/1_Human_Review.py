import streamlit as st

from db.queries import (
    get_review_queue,
    update_review_decision
)

st.set_page_config(
    page_title="Human Review Queue",
    layout="wide"
)

st.title(
    "Human Review Queue"
)

reviews = get_review_queue()

if not reviews:

    st.success(
        "No pending reviews."
    )

else:

    for review in reviews:

        with st.expander(
            f"{review.filename}"
        ):

            st.write(
                f"Predicted Category: "
                f"{review.predicted_category}"
            )

            st.write(
                f"Confidence: "
                f"{review.confidence:.2f}"
            )

            st.write(
                f"Reasoning: "
                f"{review.reasoning}"
            )

            reviewer = st.text_input(
                "Reviewer Name",
                key=f"name_{review.id}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                if st.button(
                    "Approve CEASE",
                    key=f"cease_{review.id}"
                ):

                    update_review_decision(
                        review.id,
                        reviewer,
                        "CEASE"
                    )

                    st.success(
                        "Decision saved."
                    )

                    st.rerun()

            with col2:

                if st.button(
                    "Approve IRRELEVANT",
                    key=f"irrelevant_{review.id}"
                ):

                    update_review_decision(
                        review.id,
                        reviewer,
                        "IRRELEVANT"
                    )

                    st.success(
                        "Decision saved."
                    )

                    st.rerun()
            
            with col3:
                
                if st.button(
                    "Approve DESIST",
                    key=f"desist_{review.id}"
                ):

                    update_review_decision(
                        review.id,
                        reviewer,
                        "DESIST"
                    )

                    st.rerun()
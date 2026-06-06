import csv
import os
from datetime import datetime


ARCHIVE_FILE = "archive/archive_log.csv"


def archive_agent(state):

    state["final_decision"] = "IRRELEVANT"

    file_exists = os.path.exists(
        ARCHIVE_FILE
    )

    with open(
            ARCHIVE_FILE,
            mode="a",
            newline="",
            encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow(
                [
                    "document_id",
                    "filename",
                    "decision",
                    "timestamp"
                ]
            )

        writer.writerow(
            [
                state["document_id"],
                state["filename"],
                state["final_decision"],
                datetime.now().isoformat()
            ]
        )

    print(
        f"[ARCHIVE AGENT] Archived {state['filename']}"
    )

    return state
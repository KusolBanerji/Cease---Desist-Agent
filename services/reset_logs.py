import csv
import os


ARCHIVE_FILE = (
    "archive/archive_log.csv"
)


def reset_csv_logs():

    if os.path.exists(
            ARCHIVE_FILE
    ):

        with open(
                ARCHIVE_FILE,
                "w",
                newline="",
                encoding="utf-8"
        ) as file:

            writer = csv.writer(
                file
            )

            writer.writerow(
                [
                    "document_id",
                    "filename",
                    "decision",
                    "timestamp"
                ]
            )

    print(
        "[RESET] CSV logs cleared"
    )
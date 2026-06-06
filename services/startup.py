from db.reset import (
    reset_database
)

from services.reset_logs import (
    reset_csv_logs
)

from services.reset_chroma import (
    reset_chroma
)


def initialize_application():

    reset_database()

    reset_csv_logs()

    reset_chroma()

    print(
        "\nApplication Initialized\n"
    )
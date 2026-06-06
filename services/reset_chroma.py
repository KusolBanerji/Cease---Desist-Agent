import shutil
import os


def reset_chroma():

    chroma_path = (
        "chroma_db"
    )

    if os.path.exists(
            chroma_path
    ):

        shutil.rmtree(
            chroma_path
        )

        print(
            "[RESET] ChromaDB cleared"
        )
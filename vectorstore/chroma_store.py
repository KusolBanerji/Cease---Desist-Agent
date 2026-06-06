from langchain_openai import OpenAIEmbeddings

from langchain_community.vectorstores import Chroma

from langchain_text_splitters import RecursiveCharacterTextSplitter


embeddings = OpenAIEmbeddings()


def store_document(doc_id, text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(text)
    metadatas = [
        {"document_id": doc_id}
        for _ in chunks
    ]
    db = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    db.add_texts(
        texts=chunks,
        metadatas=metadatas
    )

def get_evidence(query):
    db = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    docs = db.similarity_search(
        query,
        k=3
    )
    return [doc.page_content for doc in docs]

def clear_vector_store():

    try:
        db = Chroma(
            persist_directory="./chroma_db",
            embedding_function=embeddings
        )
        db.delete_collection()

        print(
            "[RESET] Chroma cleared"
        )

    except Exception as e:

        print(
            f"Chroma reset failed: {e}"
        )
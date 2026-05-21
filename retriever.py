import os

from langchain_community.vectorstores import Chroma

from langchain_huggingface import (
    HuggingFaceEmbeddings
)


# =========================
# Base Chroma Path
# =========================

BASE_CHROMA_PATH = "./chroma_db"


# =========================
# Embedding Model
# =========================

def get_embeddings():

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


# =========================
# Load ChromaDB
# =========================

def get_db(repo_name):

    chroma_path = (
        f"{BASE_CHROMA_PATH}/{repo_name}"
    )

    if not os.path.exists(chroma_path):

        raise FileNotFoundError(
            f"Repository DB not found at {chroma_path}"
        )

    return Chroma(
        persist_directory=chroma_path,
        embedding_function=get_embeddings()
    )


# =========================
# Advanced Retriever
# =========================

def get_retriever(
    repo_name,
    k=8
):

    db = get_db(repo_name)

    retriever = db.as_retriever(

        search_type="mmr",

        search_kwargs={

            "k": k,

            "fetch_k": 25
        }
    )

    return retriever
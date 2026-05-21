import os
import shutil
import git

from dotenv import load_dotenv

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_community.vectorstores import (
    Chroma
)

# ==========================================
# Utility Imports
# ==========================================

from utils.loaders import load_documents

from utils.chunking import split_documents


# ==========================================
# Load Environment Variables
# ==========================================

load_dotenv()


# ==========================================
# Base Paths
# ==========================================

BASE_CHROMA_PATH = "./chroma_db"

REPO_PATH = "./repo_clone"


# ==========================================
# Embedding Model
# ==========================================

def get_embeddings():

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


# ==========================================
# Clone GitHub Repository
# ==========================================

def clone_repo(repo_url):

    # Remove previous cloned repo
    if os.path.exists(REPO_PATH):

        shutil.rmtree(REPO_PATH)

    print("\nCloning repository...\n")

    # Shallow clone
    git.Repo.clone_from(
        repo_url,
        REPO_PATH,
        depth=1
    )

    print(
        "Repository cloned successfully!\n"
    )


# ==========================================
# Store Embeddings in ChromaDB
# ==========================================

def store_in_chroma(
    chunks,
    embeddings,
    chroma_path
):

    print("Generating embeddings...\n")

    db = Chroma.from_documents(

        documents=chunks,

        embedding=embeddings,

        persist_directory=chroma_path
    )

    db.persist()

    print(
        f"Embeddings stored successfully at:\n{chroma_path}\n"
    )

    return db


# ==========================================
# Main Ingestion Pipeline
# ==========================================

def ingest_repo(repo_url):

    # ======================================
    # Repository Name
    # ======================================

    repo_name = (
        repo_url.split("/")[-1]
    )

    # ======================================
    # Repo-Specific Chroma Path
    # ======================================

    chroma_path = (
        f"{BASE_CHROMA_PATH}/{repo_name}"
    )

    # ======================================
    # Cache Check
    # ======================================

    if os.path.exists(chroma_path):

        print(
            "\nRepository already indexed."
        )

        return Chroma(

            persist_directory=chroma_path,

            embedding_function=get_embeddings()
        )

    # ======================================
    # Clone Repository
    # ======================================

    clone_repo(repo_url)

    # ======================================
    # Load Documents
    # ======================================

    documents = load_documents(

        REPO_PATH,

        repo_url
    )

    if not documents:

        raise ValueError(
            "No valid documents found."
        )

    # ======================================
    # Split Documents into Chunks
    # ======================================

    chunks = split_documents(
        documents
    )

    # ======================================
    # Embedding Model
    # ======================================

    embeddings = get_embeddings()

    # ======================================
    # Store in ChromaDB
    # ======================================

    db = store_in_chroma(

        chunks,

        embeddings,

        chroma_path
    )

    print(
        "Repository ingestion completed successfully!"
    )

    return db


# ==========================================
# Direct Testing
# ==========================================

if __name__ == "__main__":

    ingest_repo(
        "https://github.com/karpathy/micrograd"
    )
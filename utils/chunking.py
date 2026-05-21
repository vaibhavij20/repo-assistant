from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    Language
)


# =========================
# Split Documents
# =========================

def split_documents(documents):

    python_docs = []

    other_docs = []

    for doc in documents:

        if doc.metadata.get(
            "extension"
        ) == ".py":

            python_docs.append(doc)

        else:

            other_docs.append(doc)

    chunks = []

    # =========================
    # Python-aware chunking
    # =========================

    if python_docs:

        python_splitter = (
            RecursiveCharacterTextSplitter
            .from_language(
                language=Language.PYTHON,
                chunk_size=1500,
                chunk_overlap=300
            )
        )

        chunks.extend(
            python_splitter.split_documents(
                python_docs
            )
        )

    # =========================
    # Generic chunking
    # =========================

    if other_docs:

        generic_splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=1500,
                chunk_overlap=300
            )
        )

        chunks.extend(
            generic_splitter.split_documents(
                other_docs
            )
        )

    print(
        f"Created {len(chunks)} chunks\n"
    )

    return chunks
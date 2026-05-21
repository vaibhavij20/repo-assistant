import os

from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader
)


# =========================
# Ignore Folders
# =========================

IGNORE_DIRS = [
    ".git",
    "node_modules",
    "venv",
    "__pycache__",
    "dist",
    "build",
    ".next",
    "coverage"
]


# =========================
# File Extensions
# =========================

EXTENSIONS = [
    "**/*.py",
    "**/*.js",
    "**/*.ts",
    "**/*.tsx",
    "**/*.java",
    "**/*.cpp",
    "**/*.c",
    "**/*.html",
    "**/*.css",
    "**/*.md",
    "**/*.json",
    "**/*.yaml",
    "**/*.yml",
    "**/*.txt"
]


# =========================
# Load Documents
# =========================

def load_documents(repo_path, repo_url):

    all_docs = []

    print("Loading repository files...\n")

    for ext in EXTENSIONS:

        loader = DirectoryLoader(
            repo_path,
            glob=ext,
            loader_cls=TextLoader,
            loader_kwargs={
                "encoding": "utf-8"
            },
            silent_errors=True
        )

        try:

            docs = loader.load()

            for doc in docs:

                source = doc.metadata.get(
                    "source",
                    ""
                )

                # Ignore noisy folders
                if any(
                    ignore in source
                    for ignore in IGNORE_DIRS
                ):
                    continue

                # Add metadata
                doc.metadata["repo"] = (
                    repo_url
                )

                doc.metadata["filename"] = (
                    os.path.basename(source)
                )

                doc.metadata["extension"] = (
                    os.path.splitext(source)[1]
                )

                all_docs.append(doc)

        except Exception as e:

            print(
                f"Error loading {ext}: {e}"
            )

    print(
        f"Loaded {len(all_docs)} documents\n"
    )

    return all_docs
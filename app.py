import os

import streamlit as st

from ingest import ingest_repo
from chain import ask, clear_memory
from utils.github_utils import get_repo_info


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Repo Assistant",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

st.title("Repo Assistant")

st.markdown(
    """
    GitHub repository intelligence system 
    """
)

st.divider()


# =========================================================
# SESSION STATE
# =========================================================

if "ingested" not in st.session_state:
    st.session_state.ingested = False

if "repo_url" not in st.session_state:
    st.session_state.repo_url = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "repo_info" not in st.session_state:
    st.session_state.repo_info = None

if "repo_summary" not in st.session_state:
    st.session_state.repo_summary = ""


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("Repository Setup")

    repo_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/owner/repo",
        value=st.session_state.repo_url
    )

    # =====================================================
    # INGEST REPOSITORY
    # =====================================================

    if st.button(
        "Ingest Repository",
        use_container_width=True
    ):

        if not repo_url.strip():

            st.error(
                "Please enter a valid GitHub URL."
            )

        else:

            with st.spinner(
                "Cloning and indexing repository..."
            ):

                try:

                    # =====================================
                    # INGEST REPO
                    # =====================================

                    ingest_repo(
                        repo_url.strip()
                    )

                    # =====================================
                    # STORE ACTIVE REPO
                    # =====================================

                    os.environ[
                        "ACTIVE_REPO_URL"
                    ] = repo_url.strip()

                    # =====================================
                    # FETCH GITHUB INFO
                    # =====================================

                    repo_info = get_repo_info(
                        repo_url.strip()
                    )

                    # =====================================
                    # SAVE SESSION STATE
                    # =====================================

                    st.session_state.ingested = True

                    st.session_state.repo_url = (
                        repo_url.strip()
                    )

                    st.session_state.repo_info = (
                        repo_info
                    )

                    st.session_state.messages = []

                    st.session_state.repo_summary = ""

                    st.success(
                        "Repository indexed successfully."
                    )

                except Exception as e:

                    st.error(
                        f"Ingestion failed: {e}"
                    )

    # =====================================================
    # ACTIVE REPOSITORY INFO
    # =====================================================

    if st.session_state.ingested:

        st.divider()

        st.subheader(
            "Active Repository"
        )

        st.code(
            st.session_state.repo_url,
            language=None
        )

        info = st.session_state.repo_info

        # =================================================
        # GITHUB METADATA
        # =================================================

        if info:

            st.markdown(
                f"Stars: {info['stars']}"
            )

            st.markdown(
                f"Forks: {info['forks']}"
            )

            st.markdown(
                f"Open Issues: {info['issues']}"
            )

            st.markdown(
                f"Watchers: {info['watchers']}"
            )

            st.markdown(
                f"Language: {info['language']}"
            )

            st.markdown(
                f"Owner: {info['owner']}"
            )

            if info["description"]:

                st.markdown(
                    "Description"
                )

                st.write(
                    info["description"]
                )

        # =================================================
        # CLEAR CHAT
        # =================================================

        if st.button(
            "Clear Chat",
            use_container_width=True
        ):

            clear_memory()

            st.session_state.messages = []

            st.success(
                "Chat cleared successfully."
            )

        # =================================================
        # RESET REPOSITORY
        # =================================================

        if st.button(
            "Reset Repository",
            use_container_width=True
        ):

            st.session_state.ingested = False

            st.session_state.repo_url = ""

            st.session_state.repo_info = None

            st.session_state.messages = []

            st.session_state.repo_summary = ""

            clear_memory()

            st.rerun()

    st.divider()

    st.markdown("How It Works")

    st.markdown(
        """
        1. Paste a GitHub repository URL  
        2. Click Ingest Repository  
        3. Repository files are chunked and embedded  
        4. Chunks are stored in ChromaDB  
        5. Semantic retrieval fetches relevant code  
        6. Gemini generates answers from repository context  
        """
    )


# =========================================================
# MAIN AREA
# =========================================================

if not st.session_state.ingested:

    st.info(
        """
        Enter a GitHub repository URL
        in the sidebar to begin.
        """
    )

    st.markdown(
        """
        ## Features

        - GitHub Repository Ingestion
        - Semantic Code Search
        - RAG-based Question Answering
        - ChromaDB Vector Database
        - HuggingFace Embeddings
        - Gemini AI Integration
        - Repository Summarization
        - Advanced MMR Retrieval
        - Language-Aware Chunking
        """
    )

    st.markdown("---")

    st.markdown(
        """
        ## Usage

        1. Paste a GitHub repository URL  
        2. Click Ingest Repository  
        3. Wait for indexing to complete  
        4. Generate repository summary  
        5. Ask questions about the codebase  
        """
    )

else:

    # =====================================================
    # REPOSITORY SUMMARY FEATURE
    # =====================================================

    st.markdown(
        "## Repository Overview"
    )

    if st.button(
        "Generate Repository Summary",
        use_container_width=True
    ):

        with st.spinner(
            "Generating repository summary..."
        ):

            try:

                summary_prompt = """
                Provide a detailed summary
                of this repository.

                Include:
                - project purpose
                - architecture
                - important modules/files
                - technologies/frameworks used
                - key classes/functions
                - workflows
                - folder structure
                """

                summary = ask(
                    summary_prompt,
                    k=12
                )

                st.session_state.repo_summary = (
                    summary
                )

            except Exception as e:

                st.error(
                    f"Summary generation failed: {e}"
                )

    # =====================================================
    # DISPLAY SUMMARY
    # =====================================================

    if st.session_state.repo_summary:

        st.markdown(
            "### Repository Summary"
        )

        st.markdown(
            st.session_state.repo_summary
        )

    st.divider()

    # =====================================================
    # CHAT HISTORY
    # =====================================================

    for msg in st.session_state.messages:

        with st.chat_message(
            msg["role"]
        ):

            st.markdown(
                msg["content"]
            )

    # =====================================================
    # CHAT INPUT
    # =====================================================

    if prompt := st.chat_input(
        "Ask anything about the repository..."
    ):

        # =================================================
        # SAVE USER MESSAGE
        # =================================================

        st.session_state.messages.append({

            "role": "user",

            "content": prompt
        })

        with st.chat_message("user"):

            st.markdown(prompt)

        # =================================================
        # GENERATE RESPONSE
        # =================================================

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "Analyzing repository..."
            ):

                try:

                    answer = ask(prompt)

                    st.markdown(answer)

                    st.session_state.messages.append({

                        "role": "assistant",

                        "content": answer
                    })

                except Exception as e:

                    error_message = (
                        f"Error generating response: {e}"
                    )

                    st.error(error_message)

                    st.session_state.messages.append({

                        "role": "assistant",

                        "content": error_message
                    })
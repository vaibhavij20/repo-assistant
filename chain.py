import os

from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

from retriever import get_retriever

# ==========================================
# Prompt Imports
# ==========================================

from utils.prompts import (
    REPO_QA_PROMPT
)


# ==========================================
# Load Environment Variables
# ==========================================

load_dotenv()

GOOGLE_API_KEY = os.getenv(
    "GOOGLE_API_KEY"
)

if not GOOGLE_API_KEY:

    raise ValueError(
        "GOOGLE_API_KEY not found in .env file"
    )


# ==========================================
# Build Gemini LLM
# ==========================================

def build_llm():

    return ChatGoogleGenerativeAI(

        model="gemini-2.5-flash",

        google_api_key=GOOGLE_API_KEY,

        temperature=0.2
    )


# ==========================================
# Main Ask Function
# ==========================================

def ask(question, k=8):

    # ======================================
    # Get Active Repository
    # ======================================

    repo_url = os.getenv(
        "ACTIVE_REPO_URL"
    )

    if not repo_url:

        return (
            "No repository is currently active."
        )

    repo_name = (
        repo_url.split("/")[-1]
    )

    # ======================================
    # Load Retriever
    # ======================================

    retriever = get_retriever(

        repo_name=repo_name,

        k=k
    )

    # ======================================
    # Retrieve Documents
    # ======================================

    docs = retriever.invoke(question)

    print(
        "\n========== RETRIEVED DOCUMENTS ==========\n"
    )

    context = ""

    for i, doc in enumerate(docs):

        source = doc.metadata.get(
            "source",
            "unknown"
        )

        print(f"\nDOCUMENT {i+1}")

        print(f"SOURCE: {source}")

        print("-" * 60)

        print(doc.page_content[:500])

        # ==================================
        # Build Context
        # ==================================

        context += (
            f"\n\nSOURCE FILE: {source}\n"
        )

        context += doc.page_content

    # ======================================
    # Build Prompt
    # ======================================

    prompt = REPO_QA_PROMPT.format(

        context=context,

        question=question
    )

    # ======================================
    # Generate Response
    # ======================================

    llm = build_llm()

    response = llm.invoke(prompt)

    return response.content


# ==========================================
# Clear Memory Placeholder
# ==========================================

def clear_memory():

    print(
        "Memory feature currently disabled."
    )


# ==========================================
# Direct Testing
# ==========================================

if __name__ == "__main__":

    os.environ[
        "ACTIVE_REPO_URL"
    ] = (
        "https://github.com/karpathy/micrograd"
    )

    while True:

        question = input(
            "\nAsk a question: "
        )

        if question.lower() == "exit":

            break

        answer = ask(question)

        print("\nANSWER:\n")

        print(answer)
# Repo Assistant

Repo Assistant is a Retrieval-Augmented Generation (RAG) based application that can understand and answer questions about any GitHub repository using semantic search, vector databases, and Gemini AI.

The project helps developers quickly explore unfamiliar codebases without manually reading hundreds of files.

---

## Features

* GitHub repository ingestion
* Semantic code search
* Repository-aware Q&A
* AI-generated repository summaries
* Language-aware chunking
* Advanced MMR retrieval
* ChromaDB caching for faster indexing
* GitHub metadata integration

---

## Tech Stack

* Python
* Streamlit
* LangChain
* ChromaDB
* HuggingFace Embeddings
* Gemini AI
* GitPython
* PyGithub

---

## How It Works

1. Clone GitHub repository
2. Load and preprocess repository files
3. Split code into semantic chunks
4. Generate embeddings
5. Store embeddings in ChromaDB
6. Retrieve relevant context
7. Generate answers using Gemini AI

---

## Architecture

```text
GitHub Repository
        ↓
Repository Loader
        ↓
Language-Aware Chunking
        ↓
Embedding Generation
        ↓
ChromaDB Vector Store
        ↓
MMR Retriever
        ↓
Gemini AI
        ↓
Repository-Aware Answers
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/vaibhavij20/repo-assistant.git
cd repo-assistant
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### macOS/Linux

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root directory and add:

```env
GEMINI_API_KEY=your_api_key
GITHUB_TOKEN=your_github_token
```

---

## Run Application

```bash
streamlit run app.py
```

---

## Project Structure

```text
repo-assistant/
│
├── app.py
├── ingest.py
├── retriever.py
├── requirements.txt
├── .env
├── chroma_db/
└── utils/
```

---

## Future Improvements

* Multi-repository support
* Hybrid search
* Agentic workflows
* Code graph visualization
* Docker deployment
* Kubernetes support
* CI/CD integration

---

## Learning Outcomes

This project helped in understanding:

* RAG architecture
* Embedding pipelines
* Vector databases
* Semantic retrieval systems
* Production AI workflows

---

## GitHub Repository

Repo Link:
https://github.com/vaibhavij20/repo-assistant

---

## License

This project is open source and available under the MIT License.

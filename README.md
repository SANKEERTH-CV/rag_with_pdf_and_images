# FinaRAG: AI Financial Document Assistant

FinaRAG is a premium, modern AI-powered financial document assistant that implements Retrieval-Augmented Generation (RAG) and Optical Character Recognition (OCR). It allows users to upload financial PDF reports or images (such as receipts, invoices, or screenshots of financial statements) and query them through an interactive, beautiful Streamlit chat interface.

---

## Key Features

- 📑 **PDF Extraction**: Efficiently loads, splits, and indexes large financial PDF reports.
- 👁️ **OCR Capabilities**: Utilizes Tesseract OCR (`pytesseract`) to extract financial data from image statements (`.png`, `.jpg`, `.jpeg`).
- 🧠 **Context-Aware Answers**: Employs LangChain and FAISS vector stores to retrieve exact document references, feeding them into Llama-3.1 via Groq to ensure accurate answers with zero hallucinations.
- 🎨 **Premium UI**: Designed with glassmorphic cards, custom typography, linear gradients, and a responsive sidebar.
- 🗑️ **Control Panel**: Visual status indicator of active database indexing and a one-click database/history reset tool.

---

## Project Structure

- `main.py`: Contains the core RAG logic (document loaders, splitters, vector store creation, and LLM query execution).
- `app.py`: The Streamlit web interface with custom styling and session state management.
- `logo.png`: Custom AI logo asset.
- `.env`: Local environment configuration (API keys).
- `pyproject.toml` / `uv.lock`: Dependency definition managed via `uv`.

---

## Installation & Setup

### Prerequisites
- **Python**: Version 3.12+ (or 3.14 if using the project defaults).
- **Tesseract OCR**: Required for image/OCR capabilities.
  - **Windows**: Download and install from [UB-Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki), and add the installation folder (e.g., `C:\Program Files\Tesseract-OCR`) to your system PATH.
  - **macOS**: Install via Homebrew: `brew install tesseract`.
  - **Linux**: Install via apt: `sudo apt install tesseract-ocr`.

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SANKEERTH-CV/rag_with_pdf_and_images.git
   cd rag_with_pdf_and_images
   ```

2. **Install Dependencies**:
   This project uses `uv` for fast package management:
   ```bash
   # Sync virtualenv and dependencies
   uv sync
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Activate Virtual Environment**:
   - **Windows**:
     ```powershell
     .venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```

5. **Run the Application**:
   Start the Streamlit server:
   ```bash
   uv run streamlit run app.py
   ```
   Open your browser and navigate to `http://localhost:8501`.

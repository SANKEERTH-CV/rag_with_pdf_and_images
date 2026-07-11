import streamlit as st
import os
import shutil
import tempfile
from PIL import Image
from main import process_document, ask_question

# Set page config
st.set_page_config(
    page_title="FinaRAG - Financial Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;800&display=swap');

/* Typography & Layout */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Gradient Header */
.main-title {
    font-family: 'Outfit', sans-serif;
    background: linear-gradient(135deg, #FF4B4B 0%, #FF8F8F 50%, #4A00E0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3.2rem;
    font-weight: 800;
    margin-bottom: 5px;
    text-align: center;
}

.subtitle {
    font-family: 'Inter', sans-serif;
    color: #888888;
    font-size: 1.2rem;
    margin-bottom: 40px;
    text-align: center;
    font-weight: 300;
}

/* Sidebar Custom Styling */
section[data-testid="stSidebar"] {
    background-color: #0E1117;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

section[data-testid="stSidebar"] .stMarkdown h2 {
    font-family: 'Outfit', sans-serif;
    color: #F8F9FA;
    font-weight: 600;
}

/* Landing Cards */
.card-container {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 30px;
}

.feature-card {
    flex: 1;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 25px;
    text-align: center;
    transition: all 0.3s ease;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5px);
}

.feature-card:hover {
    transform: translateY(-5px);
    border-color: rgba(255, 75, 75, 0.3);
    background: rgba(255, 255, 255, 0.05);
    box-shadow: 0 10px 30px rgba(255, 75, 75, 0.05);
}

.feature-icon {
    font-size: 2.5rem;
    margin-bottom: 15px;
    background: linear-gradient(135deg, #FF4B4B, #FF8F8F);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.feature-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.25rem;
    font-weight: 600;
    color: #FFFFFF;
    margin-bottom: 10px;
}

.feature-desc {
    font-size: 0.9rem;
    color: #A0AEC0;
    line-height: 1.5;
}

/* Status Badge */
.status-badge {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.2);
    color: #10B981;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
    display: inline-block;
    margin-bottom: 20px;
}

.status-badge-inactive {
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.2);
    color: #F59E0B;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
    display: inline-block;
    margin-bottom: 20px;
}

/* Chat Styling */
.stChatMessage {
    background-color: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 16px !important;
    padding: 18px !important;
    margin-bottom: 12px !important;
    transition: border 0.3s ease;
}

.stChatMessage:hover {
    border-color: rgba(255, 255, 255, 0.1) !important;
}

[data-testid="chatAvatarIcon-assistant"] {
    background: linear-gradient(135deg, #FF4B4B, #4A00E0) !important;
}

/* Info Box */
.info-box {
    background: rgba(59, 130, 246, 0.05);
    border: 1px solid rgba(59, 130, 246, 0.15);
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 25px;
    font-size: 0.95rem;
    color: #93C5FD;
}
</style>
""", unsafe_allow_html=True)

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processed_file" not in st.session_state:
    st.session_state.processed_file = None

# Sidebar Content
with st.sidebar:
    # Logo
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.title("📊 FinaRAG")
    
    st.markdown("---")
    st.markdown("## 📥 Document Upload")
    
    uploaded_file = st.file_uploader(
        "Choose a PDF or Image",
        type=["pdf", "png", "jpg", "jpeg"],
        help="Upload financial reports, statements, screenshots, or invoices"
    )
    
    # Process Uploaded File
    if uploaded_file is not None:
        file_details = {
            "Filename": uploaded_file.name,
            "Type": uploaded_file.type,
            "Size": f"{uploaded_file.size / 1024:.2f} KB"
        }
        
        # Display File details in sidebar
        st.markdown("### 📄 Selected File")
        for k, v in file_details.items():
            st.markdown(f"**{k}:** `{v}`")
            
        # Check if it needs to be processed
        if st.session_state.processed_file != uploaded_file.name:
            with st.spinner("Processing & indexing document..."):
                try:
                    # Write to a temporary file
                    suffix = os.path.splitext(uploaded_file.name)[1].lower()
                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                        temp_file.write(uploaded_file.read())
                        temp_path = temp_file.name
                    
                    # Call main.py's process_document
                    result = process_document(temp_path)
                    
                    # Clean up temporary file
                    os.unlink(temp_path)
                    
                    st.session_state.processed_file = uploaded_file.name
                    st.success("✨ Processing completed successfully!")
                    
                    # Add a system log message in the chat
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": f"📥 **System:** Successfully processed and indexed `{uploaded_file.name}`. You can now ask questions about this document!"
                    })
                    
                except Exception as e:
                    # Specific error message for missing Tesseract
                    err_str = str(e).lower()
                    if "tesseract" in err_str or "not installed" in err_str:
                        st.error(
                            "❌ Tesseract OCR is not installed or configured on the system.\n\n"
                            "Please install Tesseract-OCR and ensure it is in your system PATH to process images."
                        )
                    else:
                        st.error(f"❌ Error processing document: {str(e)}")
    
    st.markdown("---")
    st.markdown("## ⚙️ Control Panel")
    
    # Check if vector DB exists
    db_exists = os.path.exists("financial_faiss")
    
    if db_exists:
        if st.session_state.processed_file:
            st.markdown(f"🟢 **Indexed:** `{st.session_state.processed_file}`")
        else:
            st.markdown("🟢 **Indexed:** `Existing Database`")
    else:
        st.markdown("🟡 **Status:** `No Indexed Document`")
        
    if st.button("🗑️ Clear Database", use_container_width=True):
        if os.path.exists("financial_faiss"):
            try:
                shutil.rmtree("financial_faiss")
            except Exception as e:
                st.error(f"Error deleting database directory: {e}")
        st.session_state.processed_file = None
        st.session_state.messages = []
        st.success("Database and chat history cleared!")
        st.rerun()

# Main Application Layout
st.markdown('<h1 class="main-title">FinaRAG Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Intelligent financial document assistant with RAG & OCR capabilities</p>', unsafe_allow_html=True)

# Determine state
db_active = os.path.exists("financial_faiss")

if not db_active:
    # Beautiful Landing Page if database is empty
    st.markdown("""
    <div style="max-width: 800px; margin: 0 auto;">
        <div class="info-box">
            👉 <b>To get started:</b> Upload a financial PDF or an image of an invoice/statement using the file uploader in the sidebar. Once processed, you will be able to query the document directly.
        </div>
        
        <div class="card-container">
            <div class="feature-card">
                <div class="feature-icon">📂</div>
                <div class="feature-title">PDF Document Loader</div>
                <div class="feature-desc">Load large financial reports, split them into smart chunks, and index key contents seamlessly.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">👁️</div>
                <div class="feature-title">OCR Image Extraction</div>
                <div class="feature-desc">Extract financial data from screenshots of balance sheets, invoices, or charts using pytesseract.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">💬</div>
                <div class="feature-title">Contextual RAG Chat</div>
                <div class="feature-desc">Get direct answers with zero hallucinations, drawing context strictly from your uploaded files.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    # Chat Interface
    # Active document badge
    active_doc = st.session_state.processed_file or "previously loaded document"
    st.markdown(
        f'<div style="text-align: center;"><span class="status-badge">🟢 Active Context: {active_doc}</span></div>', 
        unsafe_allow_html=True
    )
    
    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    # Chat Input
    if prompt := st.chat_input("Ask a question about the document..."):
        # User message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Assistant response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            with st.spinner("Analyzing document and generating response..."):
                try:
                    response = ask_question(prompt)
                    response_placeholder.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"❌ **Error generating response:** {str(e)}"
                    response_placeholder.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

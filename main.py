from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from PIL import Image
import pytesseract
from langchain_core.documents import Document

load_dotenv()

def process_pdf(pdf_file):

    loader = PyPDFLoader(pdf_file)

    documents = loader.load()


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )


    chunks = splitter.split_documents(documents)


    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )


    vectorstore.save_local(
        "financial_faiss"
    )


    return "PDF processed successfully"


def ask_question(question):


    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


    vectorstore = FAISS.load_local(
        "financial_faiss",
        embeddings,
        allow_dangerous_deserialization=True
    )


    retriever = vectorstore.as_retriever(
        search_kwargs={"k":3}
    )


    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0
    )


    prompt = ChatPromptTemplate.from_template(
    """
    You are a financial document assistant.

    Answer only using this context:

    {context}


    Question:
    {question}
    """
    )


    def format_docs(docs):

        return "\n\n".join(
            doc.page_content
            for doc in docs
        )


    rag_chain = (
        {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
        }
        |
        prompt
        |
        llm
    )


    response = rag_chain.invoke(question)


    return response.content




def process_image(image_file):

    # Open image
    img = Image.open(image_file)


    # Extract text using OCR
    text = pytesseract.image_to_string(img)


    print("Extracted Text:")
    print(text)


    # Convert text into LangChain Document

    document = Document(
        page_content=text,
        metadata={
            "source": image_file,
            "type": "image_document"
        }
    )


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )


    chunks = splitter.split_documents(
        [document]
    )


    embeddings = HuggingFaceEmbeddings(
        model_name=
        "sentence-transformers/all-MiniLM-L6-v2"
    )


    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )


    vectorstore.save_local(
        "financial_faiss"
    )


    return "Image processed successfully"



def process_document(file):

    if file.endswith(".pdf"):

        return process_pdf(file)


    elif file.endswith(".jpg") or file.endswith(".png"):

        return process_image(file)


    else:

        return "Unsupported file type"



#using langchain
#default temperature=0.7
#adding default prompt editable text area


import streamlit as st
import fitz  # PyMuPDF for extracting text from PDFs
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage
import keys
import legal_prompt
import instructions
from langchain.text_splitter import RecursiveCharacterTextSplitter


# Configure LangChain Gemini Model
gemini_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=keys.GOOGLE_API_KEY)
# gemini_model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=keys.GOOGLE_API_KEY)

# Token limit for processing
GEMINI_MAX_TOKENS = 1000000
# GEMINI_MAX_TOKENS = 900000

# Default system prompt instructions

DEFAULT_INSTRUCTIONS = instructions.DEFAULT_PROMPT

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    """Extract text from an uploaded PDF file."""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "\n".join([page.get_text("text") for page in doc])
    return text

# Function to split text into smaller chunks
def split_text(text, chunk_size):
    """Split text into smaller chunks for processing."""
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

# def split_text(text, chunk_size=5000, overlap=200):
#     """Split text into overlapping chunks for better context retention."""
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=chunk_size, 
#         chunk_overlap=overlap,  # Overlap ensures continuity in context
#         separators=["\n\n", ". ", " "]  # Prefer breaking at paragraphs, sentences, then words
#     )
#     return splitter.split_text(text)

# Function to analyze contract risks
def analyze_contract(text, rulebook, instructions):
    """Analyze contract text using LangChain Gemini."""
    messages = [
        SystemMessage(content=instructions),
        SystemMessage(content=rulebook),
        HumanMessage(content=f"Contract Text:\n{text}")
    ]
    response = gemini_model.invoke(messages)
    return response.content if response else "No response from Gemini."

# Streamlit UI setup
st.set_page_config(page_title="LEGAL CONTRACT REVIEW: DOMESTIC ORDERS (INDIA)", layout="wide")

# Sidebar UI
with st.sidebar:
    st.image("fm-logo.png", use_container_width=True)
    st.write("Upload your Domestic Order Contracts (India) and receive an instant Legal Risk Assessment. Happy reviewing!")
    uploaded_file = st.file_uploader("Upload your contract (PDF)", type=["pdf"], key="contract")

# Editable Default Instructions Section
st.subheader("Modify Default Instructions")
instructions_text = st.text_area("Modify the default instructions as needed:", 
                                st.session_state.get("saved_instructions", DEFAULT_INSTRUCTIONS), height=300)

if st.button("Save Instructions"):
    st.session_state["saved_instructions"] = instructions_text
    st.success("Default instructions saved successfully!")

# Editable Rulebook Section
st.subheader("Modify Rulebook")
rulebook_text = st.text_area("Modify the rulebook as needed:", 
                            st.session_state.get("saved_rulebook", legal_prompt.rulebook), height=500)

if st.button("Save Rulebook"):
    st.session_state["saved_rulebook"] = rulebook_text
    st.success("Rulebook saved successfully!")

# Use saved rulebook and instructions if available
if "saved_rulebook" in st.session_state:
    rulebook_text = st.session_state["saved_rulebook"]

if "saved_instructions" in st.session_state:
    instructions_text = st.session_state["saved_instructions"]

# Main functionality
if uploaded_file and rulebook_text and instructions_text:
    with st.spinner("Extracting text from contract..."):
        contract_text = extract_text_from_pdf(uploaded_file)
    
    text_chunks = split_text(contract_text, GEMINI_MAX_TOKENS)

    if st.button("Analyze Risks"):
        with st.spinner("Analyzing contract risks..."):
            risk_analysis = "" 
            for chunk in text_chunks:
                risk_analysis += analyze_contract(chunk, rulebook_text, instructions_text) + "\n\n"
        
        st.subheader("Risk Analysis Report")
        st.write(risk_analysis)
else:
    st.info("Please upload a contract PDF and ensure the rulebook and default instructions are filled in to start analyzing.")

import streamlit as st
import fitz  # PyMuPDF for extracting text from PDFs
from legal_prompt import rulebook  # Importing the rulebook variable
from google.generativeai import configure as google_configure, GenerativeModel
import keys

# Configure Google Gemini API
google_configure(api_key=keys.GOOGLE_API_KEY)
gemini_model = GenerativeModel("gemini-1.5-flash")

# Token limit for Gemini
GEMINI_MAX_TOKENS = 1000000  # Approximate maximum for Gemini 1.5 Flash

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

# Function to analyze contract risks
def analyze_contract(text):
    """Analyze contract text using Gemini."""
    prompt = f"""
    {rulebook}
    
    Contract Text:
    {text}
    """
    response = gemini_model.generate_content(prompt)
    return response.text if response else "No response from Gemini."

# Streamlit UI setup
st.set_page_config(page_title="LEGAL CONTRACT REVIEW: DOMESTIC ORDERS (INDIA)", layout="wide")

# Sidebar UI
with st.sidebar:
    st.image("fm-logo.png", use_container_width=True)
    st.write("Upload your Domestic Order Contracts (India) and receive an instant Legal Risk Assessment. Simplify your contract review process effortlessly!**Happy reviewing!**")
    
    # File upload
    uploaded_file = st.file_uploader("Upload your contract", type=["pdf"])

# Main functionality
if uploaded_file:
    with st.spinner("Extracting text from contract..."):
        contract_text = extract_text_from_pdf(uploaded_file)
    
    # Split text into manageable chunks
    text_chunks = split_text(contract_text, GEMINI_MAX_TOKENS)

    # Analyze button
    if st.sidebar.button("Analyze Risks"):
        with st.spinner("Analyzing contract risks..."):
            risk_analysis = "" 
            
            for chunk in text_chunks:
                risk_analysis += analyze_contract(chunk) + "\n\n"
        
        st.subheader("Risk Analysis Report")
        st.write(risk_analysis)
else:
    st.info("Upload a contract PDF to start analyzing.")

import streamlit as st
import fitz  # PyMuPDF for extracting text from PDFs
from google.generativeai import configure as google_configure, GenerativeModel
import legal_prompt

# Configure Google Gemini API
google_configure(api_key=st.secrets.GOOGLE_API_KEY)
gemini_model = GenerativeModel("gemini-1.5-flash")

# Token limit for Gemini
GEMINI_MAX_TOKENS = 1000000  # Approximate maximum for Gemini 1.5 Flash

# Default prompt instructions
DEFAULT_PROMPT = """
Note: 
1. Add overall summary of the contract and risk analysis, in the end. 
2. Strictly follow the format of this rulebook and ensure that all clauses are analyzed carefully. 
3. The revised clauses must maintain legal language and should not include any explanatory 
thoughts, reasoning, or non-legal phrasing. 
4. The output should strictly adhere to the required deviation statement format, using 
strikethrough for deletions and bold for additions. 
5. Refer to entities exactly as they appear in the contract. If the contract uses "Buyer" or "Seller,"
retain those terms. If a company name is used instead, ensure it is consistently applied throughout the analysis.
"""

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
def analyze_contract(text, rulebook):
    """Analyze contract text using Gemini."""
    prompt = f"""
    {rulebook}
    
    {DEFAULT_PROMPT}
    
    Contract Text:
    {text}
    """
    # response = gemini_model.generate_content(prompt,generation_config={"temperature": 0.8})
    response = gemini_model.generate_content(prompt)
    return response.text if response else "No response from Gemini."

# Streamlit UI setup
st.set_page_config(page_title="LEGAL CONTRACT REVIEW: DOMESTIC ORDERS (INDIA)", layout="wide")

# Sidebar UI
with st.sidebar:
    st.image("fm-logo.png", use_container_width=True)
    st.write("Upload your Domestic Order Contracts (India) and receive an instant Legal Risk Assessment. Simplify your contract review process effortlessly! **Happy reviewing!**")
    
    # File upload for contract
    st.subheader("Upload Contract")
    uploaded_file = st.file_uploader("Upload your contract (PDF)", type=["pdf"], key="contract")

# Editable Rulebook Section
st.subheader("Modify Rulebook")
rulebook_text = st.text_area("Modify the rulebook as needed:",legal_prompt.rulebook, height=500)

# Save Button for Rulebook
if st.button("Save Rulebook"):
    st.session_state["saved_rulebook"] = rulebook_text
    st.success("Rulebook saved successfully!")

# Use the saved rulebook if available
if "saved_rulebook" in st.session_state:
    rulebook_text = st.session_state["saved_rulebook"]

# Main functionality
if uploaded_file and rulebook_text:
    with st.spinner("Extracting text from contract..."):
        contract_text = extract_text_from_pdf(uploaded_file)
    
    # Split text into manageable chunks
    text_chunks = split_text(contract_text, GEMINI_MAX_TOKENS)

    # Analyze button
    if st.button("Analyze Risks"):
        with st.spinner("Analyzing contract risks..."):
            risk_analysis = "" 
            
            for chunk in text_chunks:
                risk_analysis += analyze_contract(chunk, rulebook_text) + "\n\n"
        
        st.subheader("Risk Analysis Report")
        st.write(risk_analysis)
else:
    st.info("Please upload a contract PDF and ensure the rulebook is filled in to start analyzing.")

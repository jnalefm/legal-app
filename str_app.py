import streamlit as st
import fitz  # PyMuPDF for extracting text from PDFs
from legal_prompt import rulebook  # Importing the rulebook variable
from google.generativeai import configure as google_configure, GenerativeModel
import openai
import anthropic
import keys

# Configure APIs
openai.api_key = keys.OPENAI_API_KEY
anthropic_client = anthropic.Anthropic(api_key=keys.ANTHROPIC_API_KEY)
google_configure(api_key=keys.GOOGLE_API_KEY)
gemini_model = GenerativeModel("gemini-1.5-flash")

# Token limits
GPT_MAX_TOKENS = 7500  # Safe limit for GPT-4-turbo
GEMINI_MAX_TOKENS = 1000000  # Approximate maximum for Gemini 1.5 Flash
CLAUDE_MAX_TOKENS = 200000  # Approximate maximum for Claude

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
def analyze_contract(text, model_choice):
    """Analyze contract text using the selected model."""
    prompt = f"""
    {rulebook}
    
    Contract Text:
    {text}
    """
    if model_choice == "Google's Gemini Flash 1.5":
        response = gemini_model.generate_content(prompt)
        return response.text if response else "No response from Gemini."
    
    elif model_choice == "OpenAI's GPT-4":
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": rulebook},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
    
    elif model_choice == "Anthropic's Claude":
        response = anthropic_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=min(4096, len(text.split()) // 2),  # Adjusting dynamically to avoid exceeding limits
            system=rulebook,  # Pass rulebook separately
            messages=[{"role": "user", "content": text}]
        )
        return response.content[0].text if response and response.content else "No response from Claude."

# Streamlit UI setup
st.set_page_config(page_title="LEGAL CONTRACT REVIEW: DOMESTIC ORDERS (INDIA)", layout="wide")

# Sidebar UI
with st.sidebar:
    st.image("fm-logo.png", use_container_width=True)
    st.header("Upload Contract PDF")
    
    # File upload
    uploaded_file = st.file_uploader("Upload your contract", type=["pdf"])
    
    # Model selection (placed below file uploader)
    db_options = ["OpenAI's GPT-4", "Google's Gemini Flash 1.5", "Anthropic's Claude"]
    selected_model = st.selectbox("Select AI Model", db_options)

# Main functionality
if uploaded_file:
    with st.spinner("Extracting text from contract..."):
        contract_text = extract_text_from_pdf(uploaded_file)
    
    # Set chunk size based on model capabilities
    chunk_size = GPT_MAX_TOKENS if selected_model == "OpenAI's GPT-4" else (
        GEMINI_MAX_TOKENS if selected_model == "Google's Gemini Flash 1.5" else CLAUDE_MAX_TOKENS)
    
    # Split text into manageable chunks
    text_chunks = split_text(contract_text, chunk_size)

    # Analyze button
    if st.sidebar.button("Analyze Risks"):
        with st.spinner("Analyzing contract risks..."):
            risk_analysis = ""
            
            for chunk in text_chunks:
                risk_analysis += analyze_contract(chunk, selected_model) + "\n\n"
        
        st.subheader("Risk Analysis Report")
        st.write(risk_analysis)
else:
    st.info("Upload a contract PDF to start analyzing.")

import streamlit as st
import fitz  # PyMuPDF for extracting text from PDFs
import docx  # For Word document support
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage
import legal_prompt
import instructions
# import instructions_updated as instructions
from langchain.text_splitter import RecursiveCharacterTextSplitter
from google.generativeai import configure as google_configure
import keys
from io import BytesIO
import markdown
from weasyprint import HTML
import re
from google.generativeai import configure as google_configure


# Configure LangChain Gemini Model
google_configure(api_key=st.secrets.GOOGLE_API_KEY)
gemini_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Configure LangChain Gemini Model
# gemini_model = ChatGoogleGenerativeAI(
#     model="gemini-1.5-flash", 
#     google_api_key=keys.GOOGLE_API_KEY
# )

# Token limit
GEMINI_MAX_TOKENS = 1000000

# Default Instructions
DEFAULT_INSTRUCTIONS = instructions.DEFAULT_PROMPT

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "\n".join([page.get_text("text") for page in doc])
    return text

# Function to extract text from a Word file
def extract_text_from_word(word_file):
    doc = docx.Document(word_file)
    return "\n".join([para.text for para in doc.paragraphs])

# Split text into chunks
def split_text(text, chunk_size):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

# Analyze contract risks
def analyze_contract(text, rulebook, instructions):
    messages = [
        SystemMessage(content=instructions),
        SystemMessage(content=rulebook),
        HumanMessage(content=f"Contract Text:\n{text}")
    ]
    response = gemini_model.invoke(messages)
    return response.content if response else "No response from Gemini."

# Generate a PDF from markdown content with styling
def generate_pdf(content):
    html_content = markdown.markdown(
        content,
        extensions=["tables", "fenced_code", "nl2br", "smarty"]
    )

    styled_html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                font-size: 12pt;
                margin: 40px;
                line-height: 1.5;
            }}
            .header {{
                display: flex;
                align-items: center;
                margin-bottom: 20px;
            }}
            .logo {{
                width: 120px;
                height: auto;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th, td {{
                border: 1px solid #333;
                padding: 8px;
                text-align: left;
                vertical-align: top;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            strong, b {{
                font-weight: bold;
            }}
            del {{
                text-decoration: line-through;
                color: blue;
            }}
            code {{
                background-color: #f9f9f9;
                font-family: monospace;
                padding: 2px 4px;
                border-radius: 4px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <img src="fm-logo.png" alt="Logo" class="logo" />
        </div>
        {html_content}
    </body>
    </html>
    """

    pdf_io = BytesIO()
    HTML(string=styled_html, base_url=".").write_pdf(target=pdf_io)  # base_url needed for relative path to image
    pdf_io.seek(0)
    return pdf_io


# UI Setup
st.set_page_config(
    page_title="LEGAL CONTRACT REVIEW: DOMESTIC ORDERS (INDIA)", 
    layout="wide"
)

# Sidebar
with st.sidebar:
    st.image("fm-logo.png", use_container_width=True)
    st.write("Upload your Domestic Order Contracts (India) and receive an instant Legal Risk Assessment.")
    uploaded_file = st.file_uploader(
        "Upload your contract (PDF or Word)", 
        type=["pdf", "docx"], 
        key="contract"
    )

# Editable Instructions
st.subheader("Modify Default Instructions")
instructions_text = st.text_area(
    "Modify the default instructions as needed:", 
    st.session_state.get("saved_instructions", DEFAULT_INSTRUCTIONS), 
    height=300
)

if st.button("Save Instructions"):
    st.session_state["saved_instructions"] = instructions_text
    st.success("Default instructions saved successfully!")

# Editable Rulebook
st.subheader("Modify Rulebook")
rulebook_text = st.text_area(
    "Modify the rulebook as needed:", 
    st.session_state.get("saved_rulebook", legal_prompt.rulebook), 
    height=500
)

if st.button("Save Rulebook"):
    st.session_state["saved_rulebook"] = rulebook_text
    st.success("Rulebook saved successfully!")

# Load saved rulebook/instructions
if "saved_rulebook" in st.session_state:
    rulebook_text = st.session_state["saved_rulebook"]
if "saved_instructions" in st.session_state:
    instructions_text = st.session_state["saved_instructions"]

# Process uploaded file
if uploaded_file and rulebook_text and instructions_text:
    with st.spinner("Extracting text from contract..."):
        file_type = uploaded_file.name.split('.')[-1].lower()
        if file_type == "pdf":
            contract_text = extract_text_from_pdf(uploaded_file)
        elif file_type == "docx":
            contract_text = extract_text_from_word(uploaded_file)
        else:
            st.error("Unsupported file type.")
            st.stop()

    text_chunks = split_text(contract_text, GEMINI_MAX_TOKENS)

    if st.button("Analyze Risks"):
        with st.spinner("Analyzing contract risks..."):
            risk_analysis = ""
            for chunk in text_chunks:
                result = analyze_contract(chunk, rulebook_text, instructions_text)
                # Replace ~~text~~ with <del>text</del>
                result = re.sub(r"~~(.*?)~~", r"<del>\1</del>", result)
                risk_analysis += result + "\n\n"

        st.subheader("Risk Analysis Report")
        st.markdown(risk_analysis, unsafe_allow_html=True)

        # Generate downloadable PDF
        pdf_bytes = generate_pdf(risk_analysis)
        st.download_button(
            label="Download Report as PDF",
            data=pdf_bytes,
            file_name="contract_risk_analysis.pdf",
            mime="application/pdf"
        )
else:
    st.info("Please upload a contract PDF or Word file and ensure the rulebook and default instructions are filled in.")

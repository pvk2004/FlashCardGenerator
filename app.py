import streamlit as st

from utils import extract_text_from_pdf, generate_flashcards_local, generate_flashcards_with_ollama
import io
import fitz

st.title("AI Comprehensive Question Generator")
st.markdown("Generate detailed 10-mark questions and answers from PDF content")

# Sidebar for settings
st.sidebar.subheader("Settings")
num_cards = st.sidebar.slider("Number of Questions", min_value=3, max_value=15, value=5)

# Generation method selection
generation_method = st.sidebar.selectbox(
    "Generation Method",
    ["Local (Rule-based)", "Ollama (if available)"],
    help="Local: Uses pattern matching. Ollama: Uses local LLM if installed."
)

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    # Get number of pages
    pdf_bytes = uploaded_file.read()
    pdf_file = io.BytesIO(pdf_bytes)
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    num_pages = doc.page_count
    doc.close()
    st.write(f"Total pages: {num_pages}")

    # Page range selection
    start_page = st.number_input("Start Page", min_value=1, max_value=num_pages, value=1)
    end_page = st.number_input("End Page", min_value=1, max_value=num_pages, value=num_pages)

    if st.button("Extract Text"):
        pdf_file.seek(0)
        text = extract_text_from_pdf(pdf_file, (int(start_page), int(end_page)))
        st.text_area("Extracted Text", text, height=300)
        
        # Store extracted text in session state
        st.session_state.extracted_text = text
        st.session_state.text_extracted = True

def display_flashcards(flashcards, style="Flip"):
    st.subheader("Comprehensive Questions & Answers")
    if style == "Flip":
        for i, card in enumerate(flashcards, 1):
            with st.expander(f"Q{i}: {card['question']}"):
                st.markdown(f"**Answer:**")
                st.write(card['answer'])
    elif style == "List":
        for i, card in enumerate(flashcards, 1):
            st.markdown(f"**Q{i}: {card['question']}**")
            st.markdown(f"**Answer:**")
            st.write(card['answer'])
            st.markdown("---")

# Generate flashcards button (only show if text was extracted)
if hasattr(st.session_state, 'text_extracted') and st.session_state.text_extracted:
    if st.button("Generate Comprehensive Questions"):
        with st.spinner("Generating comprehensive questions..."):
            if generation_method == "Local (Rule-based)":
                flashcards = generate_flashcards_local(st.session_state.extracted_text, num_cards)
            else:  # Ollama
                flashcards = generate_flashcards_with_ollama(st.session_state.extracted_text, num_cards=num_cards)
            
            if flashcards:
                st.session_state.flashcards = flashcards
                st.success(f"Generated {len(flashcards)} comprehensive questions using {generation_method}!")
            else:
                st.error("Failed to generate questions. Please try again.")

# Display flashcards if available
if hasattr(st.session_state, 'flashcards') and st.session_state.flashcards:
    # UI to select flashcard style
    st.sidebar.subheader("Display Style")
    display_style = st.sidebar.radio("Choose style:", ["Flip", "List"])
    
    display_flashcards(st.session_state.flashcards, style=display_style)
else:
    # Show sample flashcards if no AI-generated ones
    st.sidebar.subheader("Display Style")
    display_style = st.sidebar.radio("Choose style:", ["Flip", "List"])
    
    sample_flashcards = [
        {
            "question": "Discuss in detail about Artificial Intelligence and its applications in modern technology.",
            "answer": "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines. It encompasses various technologies including machine learning, natural language processing, and robotics. AI applications include virtual assistants, autonomous vehicles, medical diagnosis, and financial analysis. The technology continues to evolve and impact various industries."
        },
        {
            "question": "Analyze and explain the key principles of machine learning and their significance in data science.",
            "answer": "Machine learning is a subset of AI that enables systems to learn and improve from experience. Key principles include supervised learning, unsupervised learning, and reinforcement learning. These principles are fundamental to data science and enable predictive modeling, pattern recognition, and automated decision-making processes."
        },
    ]
    display_flashcards(sample_flashcards, style=display_style)

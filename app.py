
import streamlit as st
from transformers import pipeline

# Page configuration
st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="✨",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>

/* Dual-tone background */
.stApp {
    background: linear-gradient(
        to bottom,
        #142D4E 0%,
        #142D4E 36%,
        #E5F3EC 36%,
        #E5F3EC 100%
    );
    background-attachment: fixed;
}

/* Main page layout */
.block-container {
    max-width: 850px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* Header card */
.header-card {
    background: #FFFFFF;
    padding: 28px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    margin-bottom: 25px;
}

.header-card h1 {
    color: #142D4E;
    font-size: 32px;
    margin-bottom: 8px;
}

.header-card p {
    color: #64748B;
    font-size: 15px;
    margin: 0;
}

/* Text and labels */
.stMarkdown, label {
    color: #142D4E !important;
    font-weight: 500;
}

/* Text input */
.stTextArea textarea {
    background-color: #FFFFFF !important;
    color: #263746 !important;
    border: 1px solid #B8CEC2 !important;
    border-radius: 13px !important;
    font-size: 15px !important;
}

/* Button */
.stButton button {
    background: #287A59 !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px !important;
    font-weight: bold !important;
}

.stButton button:hover {
    background: #1E6045 !important;
}

/* Summary output */
.summary-card {
    background: #FFFFFF;
    color: #263746;
    padding: 22px;
    border-radius: 15px;
    border-left: 5px solid #287A59;
    box-shadow: 0 5px 20px rgba(0,0,0,0.10);
    font-size: 16px;
    line-height: 1.8;
}

.footer {
    text-align: center;
    color: #64748B;
    font-size: 13px;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)


# Header
st.markdown("""
<div class="header-card">
    <h1>✨ AI Text Summarizer</h1>
    <p>Transform lengthy paragraphs into meaningful summaries.</p>
    <p>Powered by Hugging Face Transformers</p>
</div>
""", unsafe_allow_html=True)


# Load Hugging Face model
@st.cache_resource(show_spinner=False)
def load_model():
    summarizer = pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6"
    )
    return summarizer


# Text input
st.subheader("📝 Enter Your Text")

input_text = st.text_area(
    "Paste your paragraph below:",
    height=250,
    placeholder="Enter or paste a long paragraph here..."
)


# Generate summary
if st.button("✨ Generate Summary", use_container_width=True):

    if not input_text.strip():

        st.warning("Please enter some text before generating a summary.")

    elif len(input_text.split()) < 30:

        st.warning("Please enter at least 30 words.")

    else:

        try:
            with st.spinner("Loading AI model and generating summary..."):

                summarizer = load_model()

                result = summarizer(
                    input_text,
                    max_length=120,
                    min_length=25,
                    do_sample=False,
                    truncation=True
                )

                summary = result[0]["summary_text"]

            st.subheader("📄 Generated Summary")

            st.markdown(
                f'<div class="summary-card">{summary}</div>',
                unsafe_allow_html=True
            )

            st.success("Summary generated successfully!")

        except Exception as e:

            st.error("Unable to generate the summary.")

            st.markdown("**Error details:**")

            st.code(
                f"{type(e).__name__}: {str(e)}"
            )

            st.info(
                "Check your Python environment, installed libraries "
                "and internet connection. The first run downloads "
                "the Hugging Face model."
            )


# Footer
st.markdown("""
<div class="footer">
    LLM Week 7 | Hugging Face Summarization Pipeline
</div>
""", unsafe_allow_html=True)

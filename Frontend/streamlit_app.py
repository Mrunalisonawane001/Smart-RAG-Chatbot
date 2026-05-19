import streamlit as st
import requests

st.set_page_config(
    page_title="Smart RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #3b82f6 100%);
        color: white;
    }

    .main {
        background: transparent;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    h1 {
        color: #ffffff !important;
        text-align: center;
        font-size: 3.2rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
        text-shadow: 0 4px 20px rgba(0,0,0,0.25);
    }

    h3 {
        color: #dbeafe !important;
        text-align: center;
        font-size: 1.3rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020617 0%, #0f172a 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    .stTextInput input {
        background: rgba(15, 23, 42, 0.85) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 12px !important;
        font-size: 16px !important;
    }

    .stTextInput input::placeholder {
        color: #cbd5e1 !important;
    }

    .stFileUploader {
        background: rgba(15, 23, 42, 0.75);
        border-radius: 14px;
        padding: 8px;
    }

    .stButton button {
        background: linear-gradient(90deg, #2563eb, #1d4ed8);
        color: white !important;
        border: none;
        border-radius: 12px;
        height: 48px;
        width: 140px;
        font-size: 16px;
        font-weight: 700;
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.35);
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        background: linear-gradient(90deg, #1d4ed8, #1e40af);
        transform: translateY(-2px);
        color: white !important;
    }

    .question-card {
        background: rgba(255, 255, 255, 0.96);
        color: #111827;
        padding: 24px;
        border-radius: 18px;
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.18);
    }

    .question-title {
        color: #2563eb;
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 12px;
    }

    .answer-title {
        color: #ffffff;
        text-align: center;
        font-size: 32px;
        font-weight: 800;
        margin-top: 25px;
        margin-bottom: 15px;
        text-shadow: 0 3px 15px rgba(0,0,0,0.25);
    }

    .answer-card {
        background: #ffffff;
        color: #111827;
        padding: 28px;
        border-radius: 18px;
        line-height: 1.9;
        font-size: 16px;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.18);
        border-left: 6px solid #2563eb;
        margin-bottom: 25px;
    }

    .sources-title {
        color: #ffffff;
        text-align: center;
        font-size: 28px;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 15px;
        text-shadow: 0 3px 15px rgba(0,0,0,0.25);
    }

    .source-card {
        background: rgba(255, 255, 255, 0.96);
        color: #111827;
        padding: 20px 24px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        margin-bottom: 30px;
    }

    .source-item {
        padding: 8px 0;
        font-size: 15px;
        border-bottom: 1px solid #e5e7eb;
    }

    .source-item:last-child {
        border-bottom: none;
    }

    .stAlert {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Smart RAG-Based Chatbot")
st.markdown("### Upload your PDF and ask intelligent questions")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("⚙️ Project Information")
    st.write("✅ Flask API")
    st.write("✅ ChromaDB Vector Database")
    st.write("✅ HuggingFace Embeddings")
    st.write("✅ Streamlit Frontend")
    st.write("✅ PDF Question Answering")
    st.write("✅ Source References")

uploaded_file = st.file_uploader(
    "📂 Upload PDF File",
    type=["pdf"]
)

if uploaded_file is not None:
    with st.spinner("📄 Processing document..."):
        try:
            response = requests.post(
                "http://127.0.0.1:5000/upload",
                files={"file": uploaded_file}
            )

            if response.status_code == 200:
                st.success("✅ Document uploaded and indexed successfully!")
            else:
                st.error("❌ File upload failed.")
                st.write(response.text)

        except Exception as e:
            st.error(f"❌ Connection Error: {e}")

question = st.text_input(
    "💬 Ask a question from your document"
)

if st.button("Ask AI"):
    if question.strip() == "":
        st.warning("⚠️ Please enter a question.")
    else:
        with st.spinner("🤖 Generating answer..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:5000/chat",
                    json={"question": question}
                )

                if response.status_code == 200:
                    data = response.json()

                    answer = data.get("answer", "No answer generated.")
                    sources = data.get("sources", [])

                    st.session_state.messages.append({
                        "question": question,
                        "answer": answer,
                        "sources": sources
                    })
                else:
                    st.error("❌ Failed to get answer.")
                    st.write(response.text)

            except Exception as e:
                st.error(f"❌ Connection Error: {e}")

for chat in reversed(st.session_state.messages):

    st.markdown(f"""
    <div class="question-card">
        <div class="question-title">🙋 Question</div>
        <p>{chat['question']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="answer-title">🤖 Answer</div>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="answer-card">{chat["answer"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="sources-title">📚 Sources</div>', unsafe_allow_html=True)

    if chat["sources"]:
        source_html = '<div class="source-card">'

        for source in chat["sources"]:
            if isinstance(source, dict):
                page = source.get("page", "Unknown")
                file_name = source.get("source", "Unknown File")
                source_html += (
                    f'<div class="source-item">📄 Page {page} — {file_name}</div>'
                )
            else:
                source_html += (
                    f'<div class="source-item">📄 {source}</div>'
                )

        source_html += '</div>'
        st.markdown(source_html, unsafe_allow_html=True)
    else:
        st.markdown(
            '<div class="source-card"><div class="source-item">No source information available.</div></div>',
            unsafe_allow_html=True
        )
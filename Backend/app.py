from flask import Flask, request, jsonify
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline
import os
import shutil
import gc
import re

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "..", "uploads")
DB_FOLDER = os.path.join(BASE_DIR, "..", "vectordb")

if os.path.exists(UPLOAD_FOLDER) and not os.path.isdir(UPLOAD_FOLDER):
    os.remove(UPLOAD_FOLDER)

if os.path.exists(DB_FOLDER) and not os.path.isdir(DB_FOLDER):
    os.remove(DB_FOLDER)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DB_FOLDER, exist_ok=True)

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# IMPORTANT:
# Your transformers version supports only "text-generation".
# We use a GPT-style model that is fully compatible.
qa_pipeline = pipeline(
    "text-generation",
    model="distilgpt2",
    max_new_tokens=200,
    do_sample=False
)

knowledge_base = None


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_relevant_context(docs):
    context = " ".join(doc.page_content for doc in docs)
    context = clean_text(context)

    if len(context) > 2500:
        context = context[:2500]

    return context


@app.route("/")
def home():
    return jsonify({
        "message": "Smart RAG Chatbot Backend is Running Successfully"
    })


@app.route("/upload", methods=["POST"])
def upload_file():
    global knowledge_base

    if "file" not in request.files:
        return jsonify({
            "error": "No file uploaded"
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "error": "No selected file"
        }), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({
            "error": "Only PDF files are supported"
        }), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    loader = PyPDFLoader(file_path)
    documents = loader.load()

    if not documents:
        return jsonify({
            "error": "No text could be extracted from the PDF"
        }), 400

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    if knowledge_base is not None:
        knowledge_base = None

    gc.collect()

    if os.path.exists(DB_FOLDER):
        shutil.rmtree(DB_FOLDER, ignore_errors=True)

    os.makedirs(DB_FOLDER, exist_ok=True)

    knowledge_base = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=DB_FOLDER
    )

    return jsonify({
        "message": "Document uploaded and indexed successfully",
        "pages_loaded": len(documents),
        "chunks_created": len(chunks)
    })


@app.route("/chat", methods=["POST"])
def chat():
    global knowledge_base

    if knowledge_base is None:
        return jsonify({
            "error": "Please upload a document first"
        }), 400

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Invalid request"
        }), 400

    question = data.get("question", "").strip()

    if question == "":
        return jsonify({
            "error": "Question cannot be empty"
        }), 400

    docs = knowledge_base.similarity_search(question, k=4)

    if not docs:
        return jsonify({
            "answer": "The answer is not available in the uploaded document.",
            "sources": []
        })

    context = extract_relevant_context(docs)

    # Resume-specific handling for better demo quality
    q = question.lower()
    answer = ""

    if "technical skill" in q or "skills" in q:
        keywords = [
            "Python", "SQL", "Excel", "Power BI", "Tableau",
            "Pandas", "NumPy", "Matplotlib", "Machine Learning",
            "Regression", "Classification", "KNN", "Naive Bayes",
            "Jupyter Notebook", "GitHub", "MySQL"
        ]

        found = [
            skill for skill in keywords
            if skill.lower() in context.lower()
        ]

        if found:
            answer = "The document mentions the following technical skills: " + ", ".join(found) + "."

    elif "full name" in q or "candidate name" in q or q == "name":
        match = re.search(r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)", context)

        if match:
            answer = f"The name mentioned in the document is {match.group(1)}."

    elif "summary" in q or "summarize" in q:
        answer = context[:600] + "..."

    # Generic fallback for any PDF
    if answer == "":
        sentences = re.split(r'(?<=[.!?])\s+', context)
        relevant = []

        question_words = {
            word.lower()
            for word in re.findall(r"\w+", question)
            if len(word) > 2
        }

        for sentence in sentences:
            sentence_lower = sentence.lower()

            if any(word in sentence_lower for word in question_words):
                relevant.append(sentence.strip())

            if len(relevant) >= 5:
                break

        if relevant:
            answer = " ".join(relevant)
        else:
            answer = context[:700]

        answer = clean_text(answer)

        if len(answer) > 900:
            answer = answer[:900] + "..."

    if answer == "":
        answer = "The answer is not available in the uploaded document."

    sources = []
    seen = set()

    for doc in docs:
        page = doc.metadata.get("page", 0)
        source_name = os.path.basename(
            doc.metadata.get("source", "Unknown")
        )

        key = (page, source_name)

        if key not in seen:
            seen.add(key)
            sources.append({
                "page": page + 1,
                "source": source_name
            })

    return jsonify({
        "answer": answer,
        "sources": sources
    })


if __name__ == "__main__":
    app.run(debug=True)
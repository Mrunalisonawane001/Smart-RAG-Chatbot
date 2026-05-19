# Smart RAG-Based Chatbot

A Smart Retrieval-Augmented Generation (RAG) based chatbot that allows users to upload PDF documents and ask intelligent questions based on the document content. The system uses Flask for the backend API, Streamlit for the frontend interface, HuggingFace embeddings for semantic understanding, ChromaDB for vector storage, and FLAN-T5 for answer generation.

---

## Features

- Upload PDF documents
- Extract text from uploaded PDFs
- Split documents into semantic chunks
- Generate embeddings using HuggingFace
- Store embeddings in ChromaDB vector database
- Retrieve relevant document chunks using similarity search
- Generate accurate answers using FLAN-T5
- Display source references with page numbers
- User-friendly Streamlit interface
- REST API built with Flask

---

## Tech Stack

### Backend
- Python
- Flask
- LangChain
- HuggingFace Transformers
- ChromaDB

### Frontend
- Streamlit

### Embedding Model
- sentence-transformers/all-MiniLM-L6-v2

### Language Model
- google/flan-t5-base

---

## Project Structure

```text
Smart-RAG-Chatbot/
│
├── Backend/
│   └── app.py
│
├── Frontend/
│   └── streamlit_app.py
│
├── .gitignore
├── requirements.txt
└── README.md




Installation
1. Clone the Repository

git clone https://github.com/Mrunalisonawane001/Smart-RAG-Chatbot.git
cd Smart-RAG-Chatbot

2. Create a Virtual Environment

python -m venv venv

3. Activate the Virtual Environment
Windows

venv\Scripts\activate

Linux / macOS

source venv/bin/activate

4. Install Dependencies

pip install -r requirements.txt

Running the Project
Start Flask Backend

cd Backend
python app.py

Backend will run at:

http://127.0.0.1:5000

Start Streamlit Frontend

Open a new terminal and run:

cd Frontend
streamlit run streamlit_app.py

Frontend will run at:

http://localhost:8501

How to Use
Open the Streamlit application.
Upload any PDF document.
Wait until the document is indexed successfully.
Enter your question in the input box.
Click Ask AI.
View the generated answer along with source references.
Example Questions
What technical skills are mentioned?
What is the educational background?
Summarize the document.
What are the main findings?
What roles is the candidate suitable for?
What certifications are listed?
API Endpoints
GET /

Checks whether the backend is running.

Response:

{
"message": "RAG Chatbot Backend is Running"
}

POST /upload

Uploads and indexes a PDF document.

Form Data:

file: PDF document

Response:

{
"message": "Document uploaded and indexed successfully"
}

POST /chat

Answers questions based on the uploaded document.

Request Body:

{
"question": "What technical skills are mentioned?"
}

Response:

{
"answer": "The document mentions Python, SQL, Machine Learning, Power BI, Tableau, and related tools.",
"sources": [
{
"page": 1,
"source": "resume.pdf"
}
]
}

Future Enhancements
Support DOCX and TXT files
Multi-document chat
Chat history
Cloud deployment
Authentication and user management
Author

Mrunali Sonawane

Assessment Submission

This project was developed as part of the Technical Assessment for the RAG-Based Chatbot assignment.

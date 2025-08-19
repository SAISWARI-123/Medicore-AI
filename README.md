# 🩺 Medicore-AI  
*A Retrieval-Augmented Medical Chat Assistant*  

## 🔍 Introduction  
**Medicore-AI** is an intelligent medical chatbot designed to assist users in navigating complex medical literature. By leveraging **Retrieval-Augmented Generation (RAG)**, the system enhances large language models with relevant context extracted from uploaded documents such as medical textbooks, reports, or notes. This ensures that responses are not only fluent but also grounded in authoritative references, minimizing hallucinations and improving factual accuracy.  

---

## 🧠 How RAG Works  
Unlike a standard LLM that generates answers purely from its training data, RAG integrates an **external knowledge base**:  

1. **User Question** → converted into embeddings  
2. **Vector Search** → retrieves semantically similar chunks from a vector database  
3. **RAG Pipeline** → combines query + retrieved context  
4. **LLM Response** → grounded, context-aware medical answer  

This workflow allows the system to dynamically adapt to any new set of medical documents provided by the user.  

---

## ✨ Key Features  
- 📄 **PDF Uploads** – Upload medical notes, research papers, or textbooks.  
- 🔎 **Contextual Search** – Automatic text extraction, chunking, and embedding.  
- 🧬 **Smart Embeddings** – Powered by **Google/BGE models** for semantic precision.  
- 📦 **Vector Database Integration** – Uses **Pinecone** for fast retrieval.  
- ⚡ **LLM-Powered Answers** – Built on **Groq’s LLaMA3-70B** via **LangChain**.  
- 🌐 **Backend APIs** – Built with **FastAPI** for efficient Q&A and file uploads.  
- 🖥 **Streamlit Frontend** – Simple, interactive chat interface for users.  

---

## 🛠 Technology Stack  

| Component      | Technology Used |
|----------------|-----------------|
| **LLM**        | Groq API (LLaMA3-70B) |
| **Embeddings** | Google Generative AI / BGE |
| **Vector DB**  | Pinecone |
| **Framework**  | LangChain |
| **Backend**    | FastAPI |
| **Frontend**   | Streamlit |
| **Deployment** | Render |

---

## 📂 Project Structure  
    Medicore-AI/
    ├── assets/ # Sample docs & assets
    ├── client/ # Streamlit frontend
    │ ├── components/ # Chat UI, file upload, download history
    │ ├── utils/ # API calls
    │ └── app.py
    ├── server/ # FastAPI backend
    │ ├── middlewares/
    │ ├── modules/ # LLM, vector store, handlers
    │ ├── routes/ # API endpoints
    │ └── main.py
    ├── .gitignore
    ├── pyproject.toml
    └── README.md
---

## ## 🏗️ Architecture

![Medicore-AI Architecture]

## ⚡ Setup Instructions  

### 1️⃣ Clone Repository  
    ```bash
    git clone https://github.com/SAISWARI-123/Medicore-AI.git
    cd Medicore-AI

2️⃣ Backend Setup (FastAPI)
    
      cd server
      python -m venv venv
      venv\Scripts\activate  # (Linux/Mac: source venv/bin/activate)
      
      pip install -r requirements.txt
      
      Create a .env file in /server with:
      
      GOOGLE_API_KEY=your_google_key
      GROQ_API_KEY=your_groq_key
      PINECONE_API_KEY=your_pinecone_key
      Run the backend:
      uvicorn main:app --reload --port 8000

3️⃣ Frontend Setup (Streamlit)
      
      cd client
      python -m venv venv
      venv\Scripts\activate  # (Linux/Mac: source venv/bin/activate)
      pip install -r requirements.txt
      streamlit run app.py

🚀 Deployment

     Deploy on Render with the following start command:
     uvicorn main:app --host 0.0.0.0 --port 10000

🙌 Credits
    Developed by B. Saiswari Patro
    Inspired by cutting-edge ecosystems: LangChain, Groq, Pinecone, FastAPI

📜 License
  This project is licensed under the MIT License – free to use and modify with attribution.

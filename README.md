## 🏡 Real Estate Research Tool (RAG-based AI Assistant)

An intelligent **Retrieval-Augmented Generation (RAG)** powered tool designed to analyze real estate articles and provide accurate, source-backed insights for homebuyers, investors, and analysts.

---
## 📌 Overview

This project allows users to input real estate-related articles (URLs) and ask questions based on them. The system retrieves relevant information and generates **fact-based answers with proper source attribution**.
It also includes a **controlled fallback mechanism**, enabling the model to provide general insights when the answer is not found in the provided sources.

---

## ✨ Features

* 🔍 **RAG Pipeline** using LangChain
* 🌐 **Multi-URL Input** for real-time article analysis
* 📊 **Source-backed Answers** (no blind hallucinations)
* 🧠 **Custom Prompt Engineering**

  * Real estate expert tone
  * Structured output (Answer + Sources)
  * Strict control over hallucination
* ⚡ **Hybrid Response System**

  * Uses sources when available
  * Falls back to general knowledge with clear labeling
* 💻 Interactive UI (Streamlit)

---

## 🛠️ Tech Stack

* **Frontend**: Streamlit
* **Backend**: Python
* **LLM**: Google Gemini API
* **Framework**: LangChain
* **Vector Store**: FAISS
* **Embeddings**: Google / OpenAI embeddings

---

## 🧠 How It Works

1. User inputs article URLs
2. Content is loaded and split into chunks
3. Embeddings are created and stored in FAISS
4. User asks a question
5. Relevant chunks are retrieved
6. LLM generates:

   * Source-based answer OR
   * General fallback response (if data not found)

---

## 🧾 Prompt Engineering

Custom prompt ensures:

* Domain-specific responses (Real Estate Analyst)
* No hallucination from external knowledge (in strict mode)
* Transparent fallback handling
* Structured output format

---

# 🏡 Real Estate Research Tool (RAG-based AI Assistant)

An intelligent **Retrieval-Augmented Generation (RAG)** powered tool that analyzes real estate articles and provides **accurate, source-backed insights** for homebuyers, investors, and analysts.

---

## 📌 Overview

This tool allows users to input real estate-related article URLs and ask questions based on them. It retrieves relevant information using a vector database and generates **fact-based answers with proper source attribution**.

It also supports a **controlled fallback mechanism**, ensuring transparency when answers are not found in the provided sources.

---

## ✨ Features

* 🔍 **RAG Pipeline** using LangChain
* 🌐 **Multi-URL Input** for real-time article analysis
* 📊 **Source-backed Answers** (reduces hallucinations)
* 🧠 **Custom Prompt Engineering**

  * Real estate expert tone
  * Structured output (Answer + Sources)
  * Controlled hallucination behavior
* ⚡ **Hybrid Response System**

  * Uses sources when available
  * Falls back to general knowledge with clear labeling
* 💻 Interactive UI (Streamlit)

---

## 🛠️ Tech Stack

* **Frontend**: Streamlit
* **Backend**: Python
* **LLM**: Groq (Llama 3)
* **Framework**: LangChain
* **Vector Store**: ChromaDB
* **Embeddings**: HuggingFace Embeddings

---

## 🧠 How It Works

1. User inputs article URLs
2. Content is loaded using `WebBaseLoader`
3. Text is split using `RecursiveCharacterTextSplitter`
4. Embeddings are generated using HuggingFace models
5. Data is stored in **ChromaDB vector store**
6. User asks a question
7. Relevant chunks are retrieved
8. LLM (Groq) generates:

   * Source-based answer OR
   * Fallback response if data not found

---

## 🧾 Prompt Engineering

Custom prompts ensure:

* Domain-specific responses (Real Estate Analyst)
* Minimal hallucination via context grounding
* Transparent fallback handling
* Structured output format


---

## 📁 Key Components

* `WebBaseLoader` → Loads content from URLs
* `RecursiveCharacterTextSplitter` → Splits large text
* `HuggingFaceEmbeddings` → Converts text to vectors
* `Chroma` → Stores and retrieves embeddings
* `RetrievalQAWithSourcesChain` → RAG pipeline
* `ChatGroq` → Generates final answers

---



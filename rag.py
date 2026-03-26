
# from uuid import uuid4
#
# # Standard libraries
# import os
# from pathlib import Path
# from dotenv import load_dotenv
# import sentence_transformers
#
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_chroma import Chroma
# from langchain_groq import ChatGroq
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_classic.chains import RetrievalQAWithSourcesChain
#
# load_dotenv()
#
# #Constants
# CHUNK_SIZE = 1000
# EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# VECTORSTORE_DIR = Path(__file__).parent / "resources/vectorstore"
# COLLECTION_NAME = "real_estate"
#
#
# llm = None
# vector_store = None
#
# def initialize_components():
#     global llm, vector_store
#
#     if llm is None:
#         llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.9, max_tokens=5000)
#
#     if vector_store is None:
#         ef = HuggingFaceEmbeddings(
#             model_name=EMBEDDING_MODEL,
#             model_kwargs={"trust_remote_code": True}
#         )
#         vector_store = Chroma(
#             collection_name=COLLECTION_NAME,
#             embedding_function=ef,
#             persist_directory = str(VECTORSTORE_DIR)
#         )
#
#
#
# def process_urls(urls):
#     """
#     This function scraps data from a url and stores it in a vector db
#     :param urls: input urls
#     :return:
#     """
#     yield "Initializing Components..."
#     initialize_components()
#
#     yield "Resetting vector store... "
#     vector_store.reset_collection()
#
#     yield "Loading data..."
#     loader = WebBaseLoader(urls)
#     data = loader.load()
#
#     yield "Splitting text into chunks... "
#     text_splitter = RecursiveCharacterTextSplitter(
#         separators=["\n\n", "\n", ".", " "],
#         chunk_size=500,
#         chunk_overlap=100
#     )
#     docs = text_splitter.split_documents(data)
#
#     yield "Adding chunks to vector db"
#     uuids = [str(uuid4()) for _ in range(len(docs))]
#     vector_store.add_documents(docs, ids=uuids)
#
#     yield "Done adding docs to vector db"
#
# def generate_answer(query):
#     if not vector_store:
#         return RuntimeError("Vector database not initialized")
#     chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vector_store.as_retriever())
#     result = chain.invoke({"question": query}, return_only_outputs=True)
#     sources = result.get("sources", "")
#
#     return result['answer'], sources
#
#
#
# if __name__ == "__main__":
#     urls = [
#         "https://www.cnbc.com/2024/12/21/how-the-federal-reserves-rate-policy-affects-mortgages.html",
#         "https://www.cnbc.com/2024/12/20/why-mortgage-rates-jumped-despite-fed-interest-rate-cut.html"
#     ]
#     print("Processing URLs...")
#     process_urls(urls)
#
#     print("Generating answer...")
#     answer, sources = generate_answer("Tell me what was the 30 year fixed mortgage rate along with the date?")
#     print(f"Answer: {answer}")
#     print(f"Sources: {sources}")
#
from uuid import uuid4
import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.chains import RetrievalQAWithSourcesChain

# Import the custom prompts
from prompt import PROMPT, EXAMPLE_PROMPT

load_dotenv()

# Constants
CHUNK_SIZE = 500
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTORSTORE_DIR = Path(__file__).parent / "resources/vectorstore"
COLLECTION_NAME = "real_estate"

llm = None
vector_store = None


def initialize_components():
    global llm, vector_store

    if llm is None:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.9,
            max_tokens=5000
        )

    if vector_store is None:
        ef = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"trust_remote_code": True}
        )
        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=ef,
            persist_directory=str(VECTORSTORE_DIR)
        )


def process_urls(urls):
    """
    Scrapes data from URLs and stores embeddings in the vector DB.
    :param urls: list of URLs to process
    """
    yield "Initializing components..."
    initialize_components()

    yield "Resetting vector store..."
    vector_store.reset_collection()

    yield "Loading data from URLs..."
    loader = WebBaseLoader(urls)
    data = loader.load()

    yield "Splitting text into chunks..."
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " "],
        chunk_size=CHUNK_SIZE,
        chunk_overlap=100
    )
    docs = text_splitter.split_documents(data)

    yield f"Adding {len(docs)} chunks to vector DB..."
    uuids = [str(uuid4()) for _ in range(len(docs))]
    vector_store.add_documents(docs, ids=uuids)

    yield "Done! URLs processed successfully."


def generate_answer(query):
    """
    Uses the custom-prompted RetrievalQAWithSourcesChain to answer a question.
    :param query: user's question string
    :return: (answer, sources) tuple
    """
    if not vector_store:
        raise RuntimeError("Vector database not initialized. Please process URLs first.")

    chain = RetrievalQAWithSourcesChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        # ✅ Custom prompt injected here — this is the key change from the base project
        combine_prompt=PROMPT,
        document_prompt=EXAMPLE_PROMPT,
    )

    result = chain.invoke({"question": query}, return_only_outputs=True)
    sources = result.get("sources", "")
    return result["answer"], sources


if __name__ == "__main__":
    urls = [
        "https://www.cnbc.com/2024/12/21/how-the-federal-reserves-rate-policy-affects-mortgages.html",
        "https://www.cnbc.com/2024/12/20/why-mortgage-rates-jumped-despite-fed-interest-rate-cut.html"
    ]
    print("Processing URLs...")
    for status in process_urls(urls):
        print(status)

    print("\nGenerating answer...")
    answer, sources = generate_answer("What was the 30-year fixed mortgage rate along with the date?")
    print(f"Answer: {answer}")
    print(f"Sources: {sources}")
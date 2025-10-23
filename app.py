from flask import Flask, render_template, jsonify, request
# We don't need these helpers in the app, only in store_index.py
# from src.helper import load_pdf_file, filter_to_minimal_docs, text_split
from langchain_pinecone import PineconeVectorStore
from langchain_community.llms import Ollama
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os
from langchain_huggingface import HuggingFaceEmbeddings

app = Flask(__name__)

load_dotenv()
PINECONE_API_KEY = os.getenv("PINE_CONE_API")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

index_name = "medibot"
    
print("Connecting to existing Pinecone index...")
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)
print("Connected.")


# --- Setup LLM and RAG Chain ---
print("Setting up RAG chain...")
# Load the local model
chat_model = Ollama(model="llama3.2")

# Create the prompt from your prompt.py file
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}")
    ]
)

retriever = docsearch.as_retriever(search_kwargs={'k': 3})

question_answer_chain = create_stuff_documents_chain(chat_model, prompt)

rag_chain = create_retrieval_chain(retriever, question_answer_chain)
print("RAG chain ready.")


# --- Flask Routes ---

@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input_text = msg
    print(f"Received message: {input_text}")
    
    # Get the response from the RAG chain
    response = rag_chain.invoke({"input": input_text})
    
    answer = response.get("answer", "Sorry, I couldn't find an answer.")
    print(f"Response: {answer}")
    
    return str(answer)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

from dotenv import load_dotenv
import os
import time  
from src.helper import load_pdf_file, filter_to_minimal_docs, text_split
from pinecone import Pinecone, ServerlessSpec 
from langchain_pinecone import PineconeVectorStore
from langchain_community.llms import Ollama
from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()

chat_model = Ollama(model="llama3.2")

PINECONE_API_KEY = os.getenv("PINE_CONE_API")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

extracted_data = load_pdf_file(data='data/')
filter_data = filter_to_minimal_docs(extracted_data)
text_chunks = text_split(filter_data)

# Use the new HuggingFaceEmbeddings class
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medibot"

if index_name not in pc.list_indexes().names():
    print(f"Creating index '{index_name}'...")
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

    # --- FIX 1: ADD THIS WAIT LOOP ---
    # print("Waiting for index to be ready... (This may take a minute)")
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(5)
    # print("Index is ready.")
    # ---------------------------------

else:
    print(f"Index '{index_name}' already exists.")
    
# This line will no longer fail, as it only runs
# after the index is confirmed to be ready.
index = pc.Index(index_name)

docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings, 
)

print("Vector store created and documents embedded successfully.")
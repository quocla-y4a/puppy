
import os
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

index_path = os.path.join(os.path.dirname(__file__), "faiss_index")
data_path = os.path.join(os.path.dirname(__file__), "faiss_data.pkl")

# model = SentenceTransformer("all-MiniLM-L6-v2")
model = SentenceTransformer("BAAI/bge-small-en-v1.5")  # hoặc multi-qa-MiniLM-L6-cos-v1

if os.path.exists(index_path):
    index = faiss.read_index(index_path)
    with open(data_path, "rb") as f:
        documents = pickle.load(f)
else:
    index = faiss.IndexFlatL2(384)
    documents = []

def add_documents(docs):
    global documents
    texts = [doc["content"] for doc in docs]
    embeddings = model.encode(texts)
    index.add(np.array(embeddings).astype("float32"))
    documents.extend(docs)

    # Save
    faiss.write_index(index, index_path)
    with open(data_path, "wb") as f:
        pickle.dump(documents, f)

def query_similar_documents(query, top_k=8):
    if len(documents) == 0:
        print("⚠️ Chưa có dữ liệu trong FAISS index.")
        return []

    embedding = model.encode([query])
    distances, indices = index.search(np.array(embedding).astype("float32"), top_k)
    return [documents[i]["content"] for i in indices[0] if i < len(documents)]


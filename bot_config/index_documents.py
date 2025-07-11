
import os
import pickle
import faiss
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer

INDEX_PATH = "faiss_store/index.faiss"
META_PATH = "faiss_store/meta.pkl"
DATA_DIR = "knowledge_base"

CHUNK_SIZE = 600      # Số ký tự mỗi đoạn
CHUNK_OVERLAP = 150    # Số ký tự chồng lặp giữa các đoạn

def split_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def load_documents(folder_path):
    docs = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            filepath = os.path.join(folder_path, filename)
            reader = PdfReader(filepath)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
            chunks = split_text(text, CHUNK_SIZE, CHUNK_OVERLAP)

            for i, chunk in enumerate(chunks):
                docs.append({
                    "id": f"{filename}_{i}",
                    "content": chunk,
                    "metadata": {"source": filename}
                })
    return docs

def build_faiss_index():
    docs = load_documents(DATA_DIR)
    if not docs:
        print("There is no file in folder knowledge_base.")
        return

    texts = [doc["content"] for doc in docs]
    metadatas = [doc["metadata"] for doc in docs]
    # model = SentenceTransformer("all-MiniLM-L6-v2")
    model = SentenceTransformer("BAAI/bge-small-en-v1.5")  # hoặc multi-qa-MiniLM-L6-cos-v1

    # embeddings = model.encode(texts)
    embeddings = model.encode(texts, normalize_embeddings=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    os.makedirs("faiss_store", exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump({
            "texts": texts,
            "metadatas": metadatas
        }, f)

    print(f"=>> Indexed {len(texts)} pharaphase from {len(set(d['metadata']['source'] for d in docs))} document.")

if __name__ == "__main__":
    build_faiss_index()

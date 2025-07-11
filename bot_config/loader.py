
import os
import fitz  # PyMuPDF
import uuid

def load_documents(folder_path):
    documents = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()

            chunks = split_into_chunks(text)
            for chunk in chunks:
                documents.append({
                    "id": str(uuid.uuid4()),
                    "content": chunk,
                    "metadata": {"source": filename}
                })

    return documents

def split_into_chunks(text, max_tokens=500):
    import re
    sentences = re.split(r'(\.|\!|\?)\s+', text)
    chunks, chunk = [], ""
    for sentence in sentences:
        if len(chunk) + len(sentence) <= max_tokens:
            chunk += sentence + " "
        else:
            chunks.append(chunk.strip())
            chunk = sentence + " "
    if chunk:
        chunks.append(chunk.strip())
    return chunks
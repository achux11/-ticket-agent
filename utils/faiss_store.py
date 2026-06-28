import faiss
import numpy as np
import os
import json
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Paths to save index and metadata
INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "tickets.index")
META_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "tickets_meta.json")

DIMENSION = 384  # all-MiniLM-L6-v2 outputs 384 dimensions

def get_embedding(text):
    """Convert text to vector embedding"""
    embedding = model.encode([text])
    return np.array(embedding, dtype='float32')

def load_index():
    """Load existing FAISS index or create new one"""
    if os.path.exists(INDEX_PATH):
        index = faiss.read_index(INDEX_PATH)
    else:
        index = faiss.IndexFlatL2(DIMENSION)
    return index

def load_meta():
    """Load metadata (ticket titles) linked to index"""
    if os.path.exists(META_PATH):
        with open(META_PATH, 'r') as f:
            return json.load(f)
    return []

def save_index(index, meta):
    """Save index and metadata to disk"""
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, 'w') as f:
        json.dump(meta, f)

def add_ticket(ticket_id, title, description):
    """Add a new ticket to FAISS index"""
    index = load_index()
    meta = load_meta()

    # Combine title and description for embedding
    text = f"{title} {description}"
    embedding = get_embedding(text)

    # Add to index
    index.add(embedding)

    # Save metadata
    meta.append({
        "ticket_id": ticket_id,
        "title": title
    })

    save_index(index, meta)

def search_similar(query, threshold=1.0):
    """Search for similar existing tickets"""
    index = load_index()
    meta = load_meta()

    # If index is empty return nothing
    if index.ntotal == 0:
        return []

    # Get query embedding
    embedding = get_embedding(query)

    # Search top 3 similar
    k = min(3, index.ntotal)
    distances, indices = index.search(embedding, k)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx != -1 and dist < threshold:
            results.append({
                "ticket_id": meta[idx]["ticket_id"],
                "title": meta[idx]["title"],
                "similarity_score": round(float(dist), 4)
            })

    return results
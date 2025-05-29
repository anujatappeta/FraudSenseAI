from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer
import torch
import faiss
import numpy as np
import os

# Globals initialized as None for lazy loading
tokenizer = None
ai_model = None
embedder = None
faiss_index = None
known_labels = None

FAISS_INDEX_PATH = "faiss_index.idx"
LABELS_PATH = "index_labels.npy"

def load_tokenizer_and_model():
    global tokenizer, ai_model
    if tokenizer is None or ai_model is None:
        # Change model here if Roberta causes memory issues
        model_name = "roberta-base-openai-detector"
        # Alternatively: model_name = "distilbert-base-uncased"
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        ai_model = AutoModelForSequenceClassification.from_pretrained(model_name)
        ai_model.eval()  # Set model to evaluation mode

def load_embedder():
    global embedder
    if embedder is None:
        embedder = SentenceTransformer("all-MiniLM-L6-v2")

def load_faiss_index_and_labels():
    global faiss_index, known_labels
    if faiss_index is None or known_labels is None:
        if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(LABELS_PATH):
            faiss_index = faiss.read_index(FAISS_INDEX_PATH)
            known_labels = np.load(LABELS_PATH)
        else:
            faiss_index = None
            known_labels = None
            print("⚠️ FAISS index or label file not found. Similarity scoring will be disabled.")

def get_ai_likelihood_score(text: str) -> float:
    load_tokenizer_and_model()
    # Protect against very long inputs causing memory issues
    max_length = 512
    if len(text) > max_length:
        text = text[:max_length]

    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=max_length)
    with torch.no_grad():
        outputs = ai_model(**inputs)
    logits = outputs.logits
    probs = torch.softmax(logits, dim=1)
    return float(probs[0][1]) * 100  # Probability of AI-generated content

def get_similarity_score(text: str):
    load_embedder()
    load_faiss_index_and_labels()

    if faiss_index is None or known_labels is None:
        return None, None

    embedding = embedder.encode([text])
    if embedding is None or len(embedding) == 0:
        return None, None

    embedding_np = np.asarray(embedding).astype('float32')
    D, I = faiss_index.search(embedding_np, k=1)  # Search for closest vector

    if I.shape[1] == 0:
        return None, None

    label = known_labels[I[0][0]]
    similarity_score = float(1 - D[0][0]) * 100  # Convert distance to similarity %
    return int(label), similarity_score

def analyze_resume_text(text: str) -> dict:
    """
    Analyze resume text for AI-generated content and similarity to known samples.
    Returns dictionary with AI likelihood and similarity results.
    """
    ai_score = get_ai_likelihood_score(text)
    faiss_label, similarity = get_similarity_score(text)

    result = {
        "ai_likelihood_score": round(ai_score, 2),
    }

    if faiss_label is not None and similarity is not None:
        result.update({
            "similarity_score": round(similarity, 2),
            "matched_label": "Legit" if faiss_label == 1 else "Fraud"
        })

    return result

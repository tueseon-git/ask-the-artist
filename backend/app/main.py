# backend/app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
import os

# Optional: sentence-transformers import if using embeddings
try:
    from sentence_transformers import SentenceTransformer, util
    EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
except Exception:
    EMBEDDING_MODEL = None

app = FastAPI(title="Ask the Artist API")
@app.get("/")
def home():
    return {"message": "Ask-The-Artist API is running!"}

# CORS - allow your site origin (replace with your actual domain in production)
FRONTEND_ORIGINS = os.environ.get("FRONTEND_ORIGINS", "*").split(",")  # e.g. "https://yourdomain.com"
if FRONTEND_ORIGINS == ["*"]:
    allow_origins = ["*"]
else:
    allow_origins = FRONTEND_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CONTACT_LINK = os.environ.get("CONTACT_LINK", "/contact-us")  # set this in env for production

# Knowledge base - canonical answers (only these will be used)
KNOWLEDGE = {
    "artist_location": "The artist Neelam and her store are located in Dehradun, Uttarakhand, India.",
    "what_she_makes": "Neelam creates mostly resin art products but also paintings, ceramic items and other unique handmade arts.",
    "customised": "Personalised or customised resin products are available in limited categories.",
    "categories": "Resin art categories include home decoration, gifting items, resin jewellery, keychains, and Pooja/Diwali items.",
    "utilities": "Stylish utilities available include phone stands, mini storage boxes, pooja thali, keychains, cup coasters and bookmarks.",
    "youtube_gift": "If you are a subscriber of https://www.youtube.com/@art_by_neelam you can pick one free resin gift from the store.",
    "shipping": "Shipping is currently not available; items must be picked up from the store.",
    "order": "To order, please contact the artist directly via the YouTube channel: https://www.youtube.com/@art_by_neelam",
    "contact": f"For more help or special questions, contact the artist here: {CONTACT_LINK}"
}

# Short keyword map (for exact matching)
KEYWORDS = {
    "where": "artist_location",
    "dehradun": "artist_location",
    "location": "artist_location",
    "resin": "what_she_makes",
    "painting": "what_she_makes",
    "ceramic": "what_she_makes",
    "custom": "customised",
    "personal": "customised",
    "gift": "youtube_gift",
    "subscribe": "youtube_gift",
    "shipping": "shipping",
    "order": "order",
    "buy": "order",
    "contact": "contact",
    "pickup": "shipping",
    "pooja": "categories",
    "diwali": "categories",
    "jewelry": "categories",
    "utilities": "utilities",
    "phone stand": "utilities",
    "store": "artist_location"
}

class Query(BaseModel):
    message: str

# Optional: prepare embedding vectors for KNOWLEDGE sentences if embedding model present
EMBEDDINGS = None
KB_SENTENCES = list(KNOWLEDGE.values())
if EMBEDDING_MODEL is not None:
    EMBEDDINGS = EMBEDDING_MODEL.encode(KB_SENTENCES, convert_to_tensor=True)

@app.post("/chat")
def chat(q: Query) -> Dict[str, str]:
    user = q.message.strip().lower()

    # 1) quick keyword match
    for token, kb_key in KEYWORDS.items():
        if token in user:
            return {"reply": KNOWLEDGE[kb_key]}

    # 2) Optional: semantic similarity (if sentence-transformers is available)
    if EMBEDDING_MODEL is not None and EMBEDDINGS is not None:
        q_emb = EMBEDDING_MODEL.encode(user, convert_to_tensor=True)
        hits = util.semantic_search(q_emb, EMBEDDINGS, top_k=1)
        if hits and hits[0]:
            idx = hits[0][0]["corpus_id"]
            matched_sentence = KB_SENTENCES[idx]
            # find the knowledge key that contains this sentence
            for k, v in KNOWLEDGE.items():
                if v == matched_sentence:
                    return {"reply": v}

    # 3) fallback - direct contact invitation
    return {"reply": KNOWLEDGE["contact"]}

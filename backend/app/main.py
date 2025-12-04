from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
import os

# Optional embedding model
try:
    from sentence_transformers import SentenceTransformer, util
    EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
except Exception:
    EMBEDDING_MODEL = None

app = FastAPI(title="Ask the Artist API")

# Root endpoint for Render
@app.get("/")
def home():
    return {"message": "Ask-The-Artist API is running!"}

# CORS
FRONTEND_ORIGINS = os.environ.get("FRONTEND_ORIGINS", "*").split(",")
allow_origins = ["*"] if FRONTEND_ORIGINS == ["*"] else FRONTEND_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Contact link (environment override allowed)
CONTACT_LINK = os.environ.get("CONTACT_LINK", "https://tueseon.com/contact-us")

# KNOWLEDGE BASE
KNOWLEDGE = {
    "artist_location": "The artist Neelam and her store are located in Dehradun, Uttarakhand, India.",
    "what_she_makes": "Neelam creates mostly resin art products but also paintings, ceramic items and other unique handmade arts. Resin art categories include home decoration, gifting items, resin jewellery, keychains, and Pooja/Diwali items.",
    "customised": "Personalised or customised resin products are available in limited categories.",
    "categories": "Resin art categories include home decoration, gifting items, resin jewellery, keychains, and Pooja/Diwali items.",
    "utilities": "Stylish utilities available include phone stands, mini storage boxes, pooja thali, keychains, cup coasters and bookmarks.",
    "youtube_gift": "If you are a subscriber of https://www.youtube.com/@art_by_neelam you can pick one free resin gift from the store.",
    "shipping": "Shipping is currently not available; items must be picked up from the store.",
    "intro": "Hi, I am AI assistant chatbot, you can ask me for any question.",
    "exhibition": "Neelam participates in seasonal exhibitons/events, Check the below Events section for all done or upcoming exhibitions.",
    "order": "To order, please contact the artist directly via the YouTube channel: https://www.youtube.com/@art_by_neelam",
    "contact": f"For more help or special questions, contact the artist here: {CONTACT_LINK}"
}

# SIMPLE KEYWORD TRIGGERS
KEYWORDS = {
    "where": "artist_location",
    "dehradun": "artist_location",
    "location": "artist_location",
    "located": "artist_location",
    "country": "artist_location",
    "resin": "what_she_makes",
    "painting": "what_she_makes",
    "ceramic": "what_she_makes",

    "custom": "customised",
    "personal": "customised",
    "hello": "intro",
    "hi": "intro",
    "query": "intro",
    "question": "intro",
    "help": "intro",
    "what is this": "intro",
    "who are you": "intro",
    "you": "intro",

    "gift": "youtube_gift",
    "subscribe": "youtube_gift",
    "discount": "youtube_gift",
    "free": "youtube_gift",
    "deal": "youtube_gift",
    "bulk": "youtube_gift",

    "shipping": "shipping",
    "outside dehradun": "shipping",
    "not in dehradun": "shipping",
    "pickup": "shipping",

    "order": "order",
    "buy": "order",

    "contact": "contact",

    "pooja": "categories",
    "diwali": "categories",
    "jewelry": "categories",
    "resin art": "categories",
    "resin gift": "categories",
    "epoxy resin": "categories",
    "gift idea": "categories",
    "epoxy": "categories",

    "utilities": "utilities",
    "phone stand": "utilities",
    "store": "artist_location",

    "exhibition": "exhibition",
    "exhibitions": "exhibition",
    "event": "exhibition",
    "marketing": "exhibition"
}

class Query(BaseModel):
    message: str

# Load semantic embeddings
EMBEDDINGS = None
KB_SENTENCES = list(KNOWLEDGE.values())

if EMBEDDING_MODEL is not None:
    EMBEDDINGS = EMBEDDING_MODEL.encode(KB_SENTENCES, convert_to_tensor=True)

@app.post("/chat")
def chat(q: Query) -> Dict[str, str]:
    user = q.message.strip().lower()

    # 1) Keyword matching
    for token, kb_key in KEYWORDS.items():
        if token in user:
            return {"answer": KNOWLEDGE[kb_key]}

    # 2) Semantic similarity (if model loaded)
    if EMBEDDING_MODEL is not None and EMBEDDINGS is not None:
        q_emb = EMBEDDING_MODEL.encode(user, convert_to_tensor=True)
        hits = util.semantic_search(q_emb, EMBEDDINGS, top_k=1)

        if hits and hits[0]:
            idx = hits[0][0]["corpus_id"]
            matched_sentence = KB_SENTENCES[idx]
            return {"answer": matched_sentence}

    # 3) Fallback
    return {"answer": KNOWLEDGE["contact"]}

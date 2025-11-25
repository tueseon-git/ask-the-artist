# Ask the Artist — Chatbot


## Overview
A lightweight FastAPI backend + artistic chat widget to provide fixed, curated answers about Neelam's resin art store. The bot only responds from the provided knowledge base and suggests contacting the artist for anything outside that scope.


## Local run (backend)


1. Create a virtual environment and activate it.
2. `pip install -r backend/requirements.txt`
3. `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
4. Open and test the `/chat` endpoint.


## Frontend


Edit `frontend/widget.js` and set `API_BASE` to your backend URL. You can paste the HTML into a GoDaddy HTML block or host it as a static file and embed via iframe.


## Deployment
- Push `backend` to GitHub and create a Render Web Service.
- Set environment variables on Render: `FRONTEND_ORIGINS` (your domain) and `CONTACT_LINK` (full contact URL).
- Deploy and copy the public URL into `frontend/widget.js`.


## Notes
- If you want better freeform matching, install `sentence-transformers` and keep embeddings enabled. Otherwise remove it from requirements.
- In production, do not use `allow_origins=["*"]`. Use your domain(s).

# Sentiment Analyzer Backend (FastAPI)

This backend provides sentiment analysis for product reviews using FastAPI, MongoDB, and supports both OpenAI GPT and BERT (via Hugging Face Transformers).

## Features
- Submit customer feedback and get sentiment analysis (BERT by default, OpenAI optional)
- Store and retrieve feedback and sentiment results from MongoDB
- API endpoints for basic and detailed sentiment analysis

## Setup Instructions
1. Create a Python virtual environment:
   ```
   python -m venv venv
   ```
2. Activate the virtual environment:
   - On Windows:
     ```
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Start the backend server:
   ```
   python main.py
   # or for hot-reload (dev):
   uvicorn main:app --reload
   ```

## API Endpoints
- `POST /feedback` — Submit feedback, returns sentiment (default: BERT)
- `GET /feedback` — Get all feedback entries
- `POST /analyze-sentiment` — Analyze any text, choose method (`bert` or `openai`)
- `POST /analyze-sentiment-detailed` — Get detailed sentiment scores (BERT only)

## Sentiment Analysis Methods
- **BERT (default):** Uses Hugging Face Transformers for fast, local sentiment analysis
- **OpenAI GPT:** Uses OpenAI API (requires `OPENAI_API_KEY` in environment)

## Frontend Integration
- React frontend (`frontend/`) sends feedback via `POST /feedback`
- Sentiment result is displayed to the user

## Example Workflow
1. User submits review in frontend
2. Frontend sends POST to backend `/feedback`
3. Backend analyzes sentiment (BERT or OpenAI)
4. Result is stored in MongoDB and returned to frontend
5. Frontend displays sentiment result

## Requirements
- Python 3.8+
- MongoDB running locally or remotely
- (Optional) OpenAI API key for GPT-based analysis

## File Guide
- `main.py` — FastAPI app, endpoints, MongoDB, sentiment logic
- `bert_sentiment.py` — BERT sentiment analysis module
- `requirements.txt` — All dependencies

---
For full-stack details and frontend workflow, see `../frontend/README.md`.

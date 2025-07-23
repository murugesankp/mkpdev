from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from pymongo import MongoClient

import openai
import os
from bert_sentiment import analyze_sentiment_bert, analyze_sentiment_bert_detailed


# Sentiment analysis using OpenAI GPT
def analyze_sentiment_openai(text: str) -> str:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise Exception("OpenAI API key not set in environment variable OPENAI_API_KEY")
    openai.api_key = OPENAI_API_KEY
    prompt = (
        "Classify the sentiment of the following customer feedback as Positive, Negative, or Neutral:\n"
        f"Feedback: {text}\n"
        "Sentiment:"
    )
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1,
        temperature=0
    )
    sentiment = response.choices[0].text.strip().lower()
    if "positive" in sentiment:
        return "positive"
    elif "negative" in sentiment:
        return "negative"
    else:
        return "neutral"

# Default sentiment analysis function (using BERT)
def analyze_sentiment(text: str, method: str = "bert") -> str:
    """
    Analyze sentiment using the specified method.
    
    Args:
        text: Text to analyze
        method: 'bert' or 'openai'
    """
    if method == "openai":
        return analyze_sentiment_openai(text)
    else:  # default to BERT
        return analyze_sentiment_bert(text)

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URL)
db = client["sentiment_db"]
feedback_collection = db["feedback"]



app = FastAPI()
# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Feedback(BaseModel):
    customer: str
    product: str
    feedback: str
    method: Optional[str] = "bert"  # Default to BERT

class FeedbackOut(Feedback):
    sentiment: str
    
class SentimentRequest(BaseModel):
    text: str
    method: Optional[str] = "bert"

class SentimentResponse(BaseModel):
    text: str
    sentiment: str
    method: str
    
class DetailedSentimentResponse(BaseModel):
    text: str
    sentiment: str
    confidence: float
    scores: dict
    method: str
@app.post("/feedback", response_model=FeedbackOut)
def submit_feedback(feedback: Feedback):
    sentiment = analyze_sentiment(feedback.feedback, feedback.method)
    entry = feedback.dict()
    entry["sentiment"] = sentiment
    feedback_collection.insert_one(entry)
    return {**entry}

@app.get("/feedback", response_model=List[FeedbackOut])
def get_feedback():
    results = list(feedback_collection.find({}, {"_id": 0}))
    return results

@app.post("/analyze-sentiment", response_model=SentimentResponse)
def analyze_text_sentiment(request: SentimentRequest):
    """Analyze sentiment of any text using BERT or OpenAI"""
    sentiment = analyze_sentiment(request.text, request.method)
    return SentimentResponse(
        text=request.text,
        sentiment=sentiment,
        method=request.method
    )

@app.post("/analyze-sentiment-detailed", response_model=DetailedSentimentResponse)
def analyze_text_sentiment_detailed(request: SentimentRequest):
    """Get detailed sentiment analysis with confidence scores (BERT only)"""
    if request.method == "openai":
        # OpenAI doesn't provide confidence scores, so fallback to simple analysis
        sentiment = analyze_sentiment_openai(request.text)
        return DetailedSentimentResponse(
            text=request.text,
            sentiment=sentiment,
            confidence=1.0,  # OpenAI doesn't provide confidence
            scores={sentiment: 1.0},
            method=request.method
        )
    else:
        # Use BERT detailed analysis
        result = analyze_sentiment_bert_detailed(request.text)
        return DetailedSentimentResponse(
            text=request.text,
            sentiment=result["sentiment"],
            confidence=result["confidence"],
            scores=result["scores"],
            method="bert"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

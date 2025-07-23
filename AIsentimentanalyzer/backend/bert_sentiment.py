from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from typing import Dict

class BERTSentimentAnalyzer:
    def __init__(self, model_name: str = "nlptown/bert-base-multilingual-uncased-sentiment"):
        """
        Initialize BERT sentiment analyzer.
        
        Args:
            model_name: Pre-trained BERT model for sentiment analysis
                       Default uses a model trained on product reviews (1-5 stars)
        """
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.eval()  # Set to evaluation mode
        
    def predict_sentiment(self, text: str) -> Dict[str, any]:
        """
        Predict sentiment of given text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with sentiment label and confidence scores
        """
        # Tokenize the input text
        inputs = self.tokenizer(
            text, 
            return_tensors="pt", 
            truncation=True, 
            padding=True, 
            max_length=512
        )
        
        # Get model predictions
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        # Convert to numpy for easier handling
        predictions = predictions.cpu().numpy()[0]
        
        # Map predictions to sentiment labels
        # This model outputs 5 classes (1-5 stars), we'll map to positive/negative/neutral
        if self.model_name == "nlptown/bert-base-multilingual-uncased-sentiment":
            # Classes: 1 star, 2 stars, 3 stars, 4 stars, 5 stars
            # Map: 1-2 stars = negative, 3 stars = neutral, 4-5 stars = positive
            negative_score = predictions[0] + predictions[1]  # 1-2 stars
            neutral_score = predictions[2]                     # 3 stars
            positive_score = predictions[3] + predictions[4]   # 4-5 stars
            
            sentiment_scores = {
                "negative": float(negative_score),
                "neutral": float(neutral_score),
                "positive": float(positive_score)
            }
            
            # Get the sentiment with highest score
            predicted_sentiment = max(sentiment_scores, key=sentiment_scores.get)
            confidence = sentiment_scores[predicted_sentiment]
            
        else:
            # For other models, assume binary or 3-class classification
            if len(predictions) == 2:
                # Binary classification (negative, positive)
                sentiment_scores = {
                    "negative": float(predictions[0]),
                    "positive": float(predictions[1]),
                    "neutral": 0.0
                }
            else:
                # 3-class classification (negative, neutral, positive)
                sentiment_scores = {
                    "negative": float(predictions[0]),
                    "neutral": float(predictions[1]) if len(predictions) > 2 else 0.0,
                    "positive": float(predictions[-1])
                }
            
            predicted_sentiment = max(sentiment_scores, key=sentiment_scores.get)
            confidence = sentiment_scores[predicted_sentiment]
        
        return {
            "sentiment": predicted_sentiment,
            "confidence": confidence,
            "scores": sentiment_scores
        }

# Alternative BERT models you can use:
class BERTSentimentAlternatives:
    """
    Alternative BERT models for sentiment analysis
    """
    
    @staticmethod
    def get_financial_bert():
        """BERT model fine-tuned on financial data"""
        return BERTSentimentAnalyzer("ProsusAI/finbert")
    
    @staticmethod
    def get_twitter_bert():
        """BERT model fine-tuned on Twitter data"""
        return BERTSentimentAnalyzer("cardiffnlp/twitter-roberta-base-sentiment-latest")
    
    @staticmethod
    def get_general_bert():
        """General purpose sentiment analysis BERT"""
        return BERTSentimentAnalyzer("j-hartmann/emotion-english-distilroberta-base")

# Initialize the global analyzer
_bert_analyzer = None

def get_bert_analyzer() -> BERTSentimentAnalyzer:
    """Get or create the global BERT analyzer instance"""
    global _bert_analyzer
    if _bert_analyzer is None:
        _bert_analyzer = BERTSentimentAnalyzer()
    return _bert_analyzer

def analyze_sentiment_bert(text: str) -> str:
    """
    Simple function to analyze sentiment using BERT.
    Returns: 'positive', 'negative', or 'neutral'
    """
    analyzer = get_bert_analyzer()
    result = analyzer.predict_sentiment(text)
    return result["sentiment"]

def analyze_sentiment_bert_detailed(text: str) -> Dict[str, any]:
    """
    Detailed sentiment analysis using BERT.
    Returns: Dictionary with sentiment, confidence, and all scores
    """
    analyzer = get_bert_analyzer()
    return analyzer.predict_sentiment(text)

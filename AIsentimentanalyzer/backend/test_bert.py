"""
Test script for BERT sentiment analysis
"""
import sys
sys.path.append('.')

from bert_sentiment import analyze_sentiment_bert, analyze_sentiment_bert_detailed

def test_bert_sentiment():
    # Test cases
    test_texts = [
        "I love this product! It's amazing and works perfectly.",
        "This is the worst product I've ever bought. Terrible quality.",
        "The product is okay, nothing special but it works.",
        "Absolutely fantastic! Highly recommended!",
        "Not good at all, very disappointed."
    ]
    
    print("=== BERT Sentiment Analysis Test ===\n")
    
    for i, text in enumerate(test_texts, 1):
        print(f"Test {i}: {text}")
        
        # Simple analysis
        sentiment = analyze_sentiment_bert(text)
        print(f"Simple result: {sentiment}")
        
        # Detailed analysis
        detailed = analyze_sentiment_bert_detailed(text)
        print(f"Detailed result:")
        print(f"  Sentiment: {detailed['sentiment']}")
        print(f"  Confidence: {detailed['confidence']:.3f}")
        print(f"  Scores: {detailed['scores']}")
        print("-" * 50)

if __name__ == "__main__":
    test_bert_sentiment()

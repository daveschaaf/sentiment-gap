from src.analyze_sentiment import get_sentiment


def test_get_sentiment_polarity():
    """it return a sentiment value -1 to 1"""
    positive_polarity, _ = get_sentiment("This product is amazing and wonderful!")
    negative_polarity, _ = get_sentiment("This freaking sucked. The worst ever!")
    assert positive_polarity > 0
    assert negative_polarity < 0

def test_get_sentiment_subjectivity():
    """facts are less subjective than opinions"""
    _, fact_subjectivity = get_sentiment("This bottle contains whey protein")
    _, opinion_subjectivity = get_sentiment("I like corn. Corn is nice to me!")
    assert fact_subjectivity < opinion_subjectivity

def test_get_sentiment_edge_cases():
    assert get_sentiment("") == (0.0,0.0)
    assert get_sentiment(None) == (0.0,0.0)
    assert get_sentiment("ok") == (0.0,0.0)
    assert get_sentiment(123) == (0.0,0.0)

def test_get_sentiment_neutral():
    neutral, _ = get_sentiment("The item arrived on Tuesday.")
    assert neutral > -0.1 and neutral < 0.1

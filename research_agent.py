from textblob import TextBlob

def analyze_company_news(company):

    news_data = [
        f"{company} reports strong revenue growth",
        f"{company} faces regulatory scrutiny",
        f"{company} expands manufacturing capacity"
    ]

    sentiment_score = 0

    for news in news_data:
        analysis = TextBlob(news)
        sentiment_score += analysis.sentiment.polarity

    sentiment_score = sentiment_score / len(news_data)

    if sentiment_score > 0:
        risk = "Low external risk"
    elif sentiment_score > -0.2:
        risk = "Moderate risk"
    else:
        risk = "High reputational risk"

    return news_data, risk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def analyze(text):
    analyser = SentimentIntensityAnalyzer()
    score = analyser.polarity_scores(text)
    return score['compound']

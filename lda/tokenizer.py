import re
import string


def tokenize(text):
    # Removing url's
    pattern = r"http\S+"

    tokens = re.sub(pattern, "", text)  # https://www.youtube.com/watch?v=O2onA4r5UaY
    tokens = re.sub('[^a-zA-Z 0-9]', '', text)
    tokens = re.sub('[%s]' % re.escape(string.punctuation), '', text)  # Remove punctuation
    tokens = re.sub('\w*\d\w*', '', text)  # Remove words containing numbers
    tokens = re.sub('@*!*\$*', '', text)  # Remove @ ! $
    tokens = tokens.strip(',')  # TESTING THIS LINE
    tokens = tokens.strip('?')  # TESTING THIS LINE
    tokens = tokens.strip('!')  # TESTING THIS LINE
    tokens = tokens.strip("'")  # TESTING THIS LINE
    tokens = tokens.strip(".")  # TESTING THIS LINE

    tokens = tokens.lower().split()  # Make text lowercase and split it

    return tokens


# Apply tokenizer
def tokenize_text(df):
    df['lemma_tokens'] = df['lemmas_back_to_text'].apply(tokenize)

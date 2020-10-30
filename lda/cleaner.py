import emoji
import re


def clean_emoji(text):
    emoji_list = [c for c in text if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.split() if not any(i in str for i in emoji_list)])
    return clean_text


def clean_url(text):
    '''
    Cleans text from urls
    '''
    text = re.sub(r'http\S+', '', text)
    return text


def clean(df):
    # Apply the function above and get tweets free of emoji's
    call_emoji_free = lambda x: clean_emoji(x)

    # Apply `call_emoji_free` which calls the function to remove all emoji's
    df['emoji_free_tweets'] = df['text'].apply(call_emoji_free)

    # Create a new column with url free tweets
    df['url_free_tweets'] = df['emoji_free_tweets'].apply(clean_url)


def remove_stopwords(df, tokenizer, ALL_STOP_WORDS):
    tokens = []

    for doc in tokenizer.pipe(df['url_free_tweets'], batch_size=500):
        doc_tokens = []
        for token in doc:
            if token.text.lower() not in ALL_STOP_WORDS:
                doc_tokens.append(token.text.lower())
        tokens.append(doc_tokens)

    # Makes tokens column
    df['tokens'] = tokens

    # Make tokens a string again
    df['tokens_back_to_text'] = [' '.join(map(str, l)) for l in df['tokens']]


def get_lemmas(text, nlp):
    lemmas = []

    doc = nlp(text)

    # Something goes here :P
    for token in doc:
        if ((token.is_stop == False) and (token.is_punct == False)) and (token.pos_ != 'PRON'):
            lemmas.append(token.lemma_)

    return lemmas


def lemmas(df, nlp):
    df['lemmas'] = df['tokens_back_to_text'].apply(get_lemmas, nlp=nlp)
    df['lemmas_back_to_text'] = [' '.join(map(str, l)) for l in df['lemmas']]

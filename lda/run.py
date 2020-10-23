import json
import pandas as pd
import emoji
import re

import pyLDAvis.gensim
import spacy
from spacy.tokenizer import Tokenizer
import string
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from gensim.corpora import Dictionary
from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD
from gensim.models.coherencemodel import CoherenceModel
from sklearn.model_selection import GridSearchCV
from gensim.models.ldamulticore import LdaMulticore
from gensim.parsing.preprocessing import STOPWORDS as SW
from wordcloud import STOPWORDS
import os
stopwords = set(STOPWORDS)

data = []
for dir in os.listdir('/home/marco/Scrivania/tirocinio-unicredit/tweets-data/hashtag/'):
    dir = '2020-10-21'
    for filename in os.listdir(f"/home/marco/Scrivania/tirocinio-unicredit/tweets-data/hashtag/{dir}/"):
        file = open(f"/home/marco/Scrivania/tirocinio-unicredit/tweets-data/hashtag/{dir}/" + filename)
        parsed_file = json.load(file)
        data += parsed_file['data']

#data = json.load(open('/home/marco/Scrivania/tirocinio-unicredit/tweets-data/hashtag/2020-10-21/JUVE.json'))
df = pd.DataFrame(data)

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

# Apply the function above and get tweets free of emoji's
call_emoji_free = lambda x: clean_emoji(x)

# Apply `call_emoji_free` which calls the function to remove all emoji's
df['emoji_free_tweets'] = df['text'].apply(call_emoji_free)

#Create a new column with url free tweets
df['url_free_tweets'] = df['emoji_free_tweets'].apply(clean_url)

print()

nlp = spacy.load('it')
tokenizer = Tokenizer(nlp.vocab)
# Custom stopwords
custom_stopwords = ['hi', '\n', '\n\n', '&amp;', ' ', '.', '-', 'got', "it's", 'it’s', "i'm", 'i’m', 'im', 'want', 'like', '$', '@']

# Customize stop words by adding to the default list
STOP_WORDS = nlp.Defaults.stop_words.union(custom_stopwords)

# ALL_STOP_WORDS = spacy + gensim + wordcloud
ALL_STOP_WORDS = STOP_WORDS.union(SW).union(stopwords)


tokens = []

for doc in tokenizer.pipe(df['url_free_tweets'], batch_size=500):
    doc_tokens = []
    for token in doc:
        if token.text.lower() not in ALL_STOP_WORDS:
            doc_tokens.append(token.text.lower())
    tokens.append(doc_tokens)

# Makes tokens column
df['tokens'] = tokens
print()

# Make tokens a string again
df['tokens_back_to_text'] = [' '.join(map(str, l)) for l in df['tokens']]


def get_lemmas(text):
    lemmas = []

    doc = nlp(text)

    # Something goes here :P
    for token in doc:
        if ((token.is_stop == False) and (token.is_punct == False)) and (token.pos_ != 'PRON'):
            lemmas.append(token.lemma_)

    return lemmas


df['lemmas'] = df['tokens_back_to_text'].apply(get_lemmas)

# Make lemmas a string again
df['lemmas_back_to_text'] = [' '.join(map(str, l)) for l in df['lemmas']]
a=0

# Tokenizer function
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
df['lemma_tokens'] = df['lemmas_back_to_text'].apply(tokenize)

print()

# Create a id2word dictionary
id2word = Dictionary(df['lemma_tokens'])
print(len(id2word))

# Filtering Extremes
id2word.filter_extremes(no_below=2, no_above=.99)
print(len(id2word))

# Creating a corpus object
corpus = [id2word.doc2bow(d) for d in df['lemma_tokens']]

# Instantiating a Base LDA model
base_model = LdaMulticore(corpus=corpus, num_topics=5, id2word=id2word, workers=12, passes=5)

# Filtering for words
words = [re.findall(r'"([^"]*)"',t[1]) for t in base_model.print_topics()]

# Create Topics
topics = [' '.join(t[0:10]) for t in words]


# Getting the topics
for id, t in enumerate(topics):
    print(f"------ Topic {id} ------")
    print(t, end="\n\n")

print()

# Compute Perplexity
# a measure of how good the model is. lower the better
base_perplexity = base_model.log_perplexity(corpus)
print('\nPerplexity: ', base_perplexity)


# Compute Coherence Score
coherence_model = CoherenceModel(model=base_model, texts=df['lemma_tokens'],
                                   dictionary=id2word, coherence='c_v')
coherence_lda_model_base = coherence_model.get_coherence()
print('\nCoherence Score: ', coherence_lda_model_base)
print()
lda_display = pyLDAvis.gensim.prepare(base_model, corpus, id2word)
d = pyLDAvis.display(lda_display)

f = open('/home/marco/Scrivania/index.html', 'w')
f.write(d.data)
f.close()

vectorizer = CountVectorizer()
data_vectorized = vectorizer.fit_transform(df['lemmas_back_to_text'])

# Define Search Param
search_params = {'n_components': [10, 15, 20, 25, 30], 'learning_decay': [.5, .7, .9]}

# Init the Model
lda = LatentDirichletAllocation()

# Init Grid Search Class
model = GridSearchCV(lda, param_grid=search_params)

# Do the Grid Search
model.fit(data_vectorized)
GridSearchCV(cv=None, error_score='raise',
             estimator=LatentDirichletAllocation(batch_size=128,
                                                 doc_topic_prior=None,
                                                 evaluate_every=-1,
                                                 learning_decay=0.7,
                                                 learning_method=None,
                                                 learning_offset=10.0,
                                                 max_doc_update_iter=100,
                                                 max_iter=10,
                                                 mean_change_tol=0.001,
                                                 n_components=10,
                                                 n_jobs=1,
                                                 perp_tol=0.1,
                                                 random_state=None,
                                                 topic_word_prior=None,
                                                 total_samples=1000000.0,
                                                 verbose=0),
             iid=True, n_jobs=1,
             param_grid={'n_topics': [10, 15, 20, 30],
                         'learning_decay': [0.5, 0.7, 0.9]},
             pre_dispatch='2*n_jobs', refit=True, return_train_score='warn',
             scoring=None, verbose=0)

# Best Model
best_lda_model = model.best_estimator_

# Model Parameters
print("Best Model's Params: ", model.best_params_)

# Log Likelihood Score
print("Best Log Likelihood Score: ", model.best_score_)

# Perplexity
print("Model Perplexity: ", best_lda_model.perplexity(data_vectorized))

print()
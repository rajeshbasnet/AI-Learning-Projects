from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

corpus = [
    'This is the first document.',
    'This document is the second document.',
    'And this is the third one.',
    'Is this the first document?',
]

tfidf_vectorizer = TfidfVectorizer()
x = tfidf_vectorizer.fit_transform(corpus)
print(tfidf_vectorizer.get_feature_names_out())

df = pd.DataFrame(x.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
print(df)

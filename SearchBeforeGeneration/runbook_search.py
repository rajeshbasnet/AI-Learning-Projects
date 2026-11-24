import re

from sklearn.feature_extraction.text import TfidfVectorizer
from runbook_finder import load_chunks
from sklearn.metrics.pairwise import cosine_similarity

from search_result import SearchResult

def search_tfidf(query:str, chunks:list[dict[str, str|bool|None]], k=3):
    ## Filter inactive section
    active_chunks = [chunk for chunk in chunks if chunk["active"] == True]
    sections = [f"{chunk["heading"]} {chunk["text"]}" for chunk in active_chunks]

    vectorizer = TfidfVectorizer(tokenizer=_tokenize, token_pattern=None, lowercase=True)
    section_matrix = vectorizer.fit_transform(sections)
    query_vector = vectorizer.transform([query])

    scores = cosine_similarity(query_vector, section_matrix).flatten()

    ## The scores generated as based on chunks order so score[0] is pointing to
    ## active_chunks[0]
    for index, score in enumerate(scores, start=0):
        if score <=0:
            continue

        result = SearchResult(
            score=score,
            source=active_chunks[index]["heading"],
            excerpt=active_chunks[index]["text"]
        )

        print(result)

def _tokenize(value:str) -> list[str]:
    return re.findall("[a-z0-9]+(?:-[a-z0-9]+)*", value)


if __name__ == "__main__":
    q = "EXP-104 export limit"
    search_tfidf(query=q, chunks=load_chunks())


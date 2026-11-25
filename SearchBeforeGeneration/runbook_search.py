import json
import re
import sys

from dataclasses import asdict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from search_result import SearchResult
from runbook_finder import load_chunks
from runbook_finder import search_overlap_call

def search_tfidf(query:str, chunks:list[dict[str, str|bool|None]], k=3):
    ## Filter inactive section
    active_chunks = [chunk for chunk in chunks if chunk["active"] == True]
    sections = [f"{chunk["heading"]} {chunk["text"]}" for chunk in active_chunks]

    vectorizer = TfidfVectorizer(tokenizer=_tokenize, token_pattern=None, lowercase=True)
    section_matrix = vectorizer.fit_transform(sections)
    query_vector = vectorizer.transform([query])

    scores = cosine_similarity(query_vector, section_matrix).flatten()
    results:list[SearchResult] = []

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
        results.append(result)

    if len(results) <= 0:
        print("No matching records found.")

    return json.dumps([asdict(res) for res in results], indent=2, ensure_ascii=False)

def _tokenize(value:str) -> list[str]:
    return re.findall("[a-z0-9]+(?:-[a-z0-9]+)*", value)


if __name__ == "__main__":
    query_re = sys.argv[1].strip()
    ranker = sys.argv[3].strip()

    if not query_re:
        raise ValueError("Invalid run command. Argument 'query' missing")

    if ranker == "overlap":
        print(search_overlap_call())
    else:
        print(search_tfidf(query=query_re, chunks=load_chunks()))

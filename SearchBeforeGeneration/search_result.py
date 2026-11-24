from dataclasses import dataclass

@dataclass()
class SearchResult:
    score:float | int = 0
    source:str = ""
    excerpt:str = ""
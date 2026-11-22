from dataclasses import dataclass


@dataclass
class Section:
    id:str = ""
    parent_id:str = ""
    path: str = ""
    version: int = 0
    active:str = ""
    heading:str = ""
    text:str = ""
    
    
    
    
    
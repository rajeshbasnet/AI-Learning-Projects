"""
There is handbook. Each handbook has 5 pages {backup, billing, login, exports, exports_archive}.md
Each page has short heading and policy which is given in problem

fixtures/handbook_manifest.json - a manifest file containing pages links (path, version, active)
exports_archive should be inactive since it's old
"""



"""
load_chunks(manifest_file_path) - if manifest malformed, report filename and underlying error
Read markdown file line by line - heading, text. Markdown containing two sections should contain
                                two records. Skip sections that contain empty body
Section  - id(<markdown_file_name>#<lowercase_heading_replaced_by_hyphens>)
        - parent_id
        - path
        - version
        - active
        - heading (Repeating headings for one file will collide id) - use order (-2, -3 depending on order)
        - text
"""

import json
from pathlib import Path
from section import Section
from dataclasses import asdict

MANIFEST_FILE_NAME = "handbook_manifest.json"
MANIFEST_FILE_PATH = f"./fixtures/{MANIFEST_FILE_NAME}"

def load_chunks():
    manifest_file_path = Path(MANIFEST_FILE_PATH)
    sections_json_list: list[dict] = []

    if not manifest_file_path.exists():
        raise ValueError(f"Manifest file ({MANIFEST_FILE_NAME}) doesn't exist")
    
    with open(MANIFEST_FILE_PATH, "r", encoding="UTF-8") as manifest_file:
        manifest_json:list[dict] = json.load(manifest_file)
        
        for document in manifest_json:
            document_path_str = document["path"]
            document_path = Path(document_path_str)
            
            if not document_path_str:
                raise ValueError("[Missing Path] Invalid manifest file.")
            elif not document_path.exists():
                raise ValueError(f"[Invalid Path]. Path: {document_path_str}")
            
            document_version = document["version"]
            document_active_status = document["active"]
            document_filename = document_path.name
            
            
            with open(document_path_str, mode="r", encoding="UTF-8") as manifest_document_file:
                sections:list[Section] = []
                heading = None
                body_lines:list = []
                
                for raw in manifest_document_file:
                    line = raw.rstrip("\r\n")
                    
                    if line.startswith("##") and not line.startswith("###"):
                        if heading is not None:
                            body = ("\n".join(body_lines)).strip()
                            section_id = f"{document_filename}#{heading.replace(" ", "-")}"
                            
                            section = Section(
                                id=section_id,
                                parent_id=section_id,
                                path=document_path_str,
                                version=document_version,
                                active=document_active_status,
                                heading=heading,
                                text=body
                            )
                            _add_sections(sections, section=section)
                            
                        heading = line[2:].strip()
                        body_lines = []
                    elif heading is not None:
                        body_lines.append(line)
            
            if heading is not None:
                body = "\n".join(body_lines)
                section_id = f"{document_filename}#{heading.replace(" ", "-")}"
                section = Section(
                                id=section_id,
                                parent_id=section_id,
                                path=document_path_str,
                                version=document_version,
                                active=document_active_status,
                                heading=heading,
                                text=body
                )
                _add_sections(sections, section=section)
                        
            _convert_section_to_json(sections_json_list, sections=sections)

    return sections_json_list


def _convert_section_to_json(final_section:list[dict], sections:list[Section]):
    section_list:list[dict] = [asdict(section) for section in sections]
    final_section.extend(section_list)

def _add_sections(sections:list, section:Section):
    sections.append(section)
            
"""
Implement word overlap first
tokenize() using regex - EXP-104 (check this type of pattern too)
"""   

import re 

def tokenize(text:str):
    text_lc = text.lower()
    tokenized_text = re.findall("[a-z0-9]+(?:-[a-z0-9]+)*", text_lc)
    return tokenized_text


"""
query = "EXP-104 export limit" - what users send
chunks:list = final json from load_chunks() which contains metadata (id, heading, text, active)
    - section from each chunk should be active only
    - join heading + " " + text and tokenize the whole - we get chunks_tokens
    - tokenize query - we get query_tokens
    - overlap the tokens to find score
"""
def search_overlap(query:str, chunks:list[dict], k = 3):
    query_tokens = set[str](tokenize(query))
    results:list[dict] = []

    for chunk in chunks:
        result:dict = {}
        if not chunk["active"]:
            continue

        heading = chunk["heading"]
        text = chunk["text"]
        section = heading + " " + text
        chunk_tokens = set[str](tokenize(section))

        score = len(query_tokens.intersection(chunk_tokens))
        if score == 0:
            continue

        source = chunk["id"]
        excerpt = chunk["text"]

        result["score"] = score
        result["source"] = source
        result["excerpt"] = excerpt
        results.append(result)

    return json.dumps(results, indent=2, ensure_ascii=False)

import sys

if __name__ == "__main__":
    chunks_re = load_chunks()
    query_re = sys.argv[1].strip()
    re = search_overlap(query_re, chunks_re)
    print(re)
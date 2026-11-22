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
                sections:list = []
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
                        
            _convert_section_to_json(sections=sections)     
 
def _convert_section_to_json(sections:list[Section]):
    section_list:list[dict] = [asdict(section) for section in sections]
    section_json = json.dumps(section_list, indent=2, ensure_ascii=False)
    print(section_json)
                        
                        
def _add_sections(sections:list, section:Section):
    sections.append(section)
            
            
            
if __name__ == "__main__":
    load_chunks()
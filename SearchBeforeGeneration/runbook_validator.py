"""
First we list all the unique ids created merging filename#heading
Validator - validate if all fields in search_dev.jsonl are valid
          - id:str, question:str, expected_sections:list, slice:str
          - verify non-empty expected IDS:ids from expected sections against parent_ids
            generated from runbook_finder
          - Do not reject an empty expected_sections
Copy fixture - copy search_dev.json to search_dev_broken.jsonl
             - Make an edit to expected section ids with random headings e.g. Backup.md#LaptopManagement (invalid value)
"""

import sys
import json

from runbook_finder import load_chunks

SECTION_EMPTY = "SECTION_EMPTY"
UNSUPPORTED_SOURCE_ID = "UNSUPPORTED_SOURCE_ID"
VALID_SOURCE_ID = "VALID_SOURCE_ID"

def _load_ids_from_chunks() -> list:
    active_chunks_ids = [chunk["id"].lower() for chunk in load_chunks() if chunk["active"]]
    return active_chunks_ids

# id, question, expected_sections, slice
def _validate_question(questions) -> None:
    if not isinstance(questions["id"], str):
        raise ValueError(f"Invalid id type. {type(questions["id "])}")

    if not isinstance(questions["question"], str):
        raise ValueError(f"Invalid id type. {type(questions["question"])}")

    if not isinstance(questions["slice"], str):
        raise ValueError(f"Invalid id type. {type(questions["slice"])}")

    if not isinstance(questions["expected_sections"], list):
        raise ValueError(f"Invalid id type. {type(questions["expected_sections"])}")

def _validate_source_id(expected_sections:list[str], active_chunk_ids:list[str]) -> str:
    for section in expected_sections:
        if not section:
            return SECTION_EMPTY
        elif not section in active_chunk_ids:
            return UNSUPPORTED_SOURCE_ID
    return VALID_SOURCE_ID

def validate_search_cases():
    search_dev_file_path = sys.argv[1]
    active_chunk_ids = _load_ids_from_chunks()

    with open(search_dev_file_path, "r", encoding="UTF-8") as search_dev_file:
        for line_number, line in enumerate(search_dev_file, start=1):
            if not line:
                print(f"Skipping empty line number: {line_number}")
                continue

            question_json = json.loads(line)
            _validate_question(question_json)

            # check if expected sections has valid id using for loop
            expected_sections = question_json['expected_sections']
            validate_output = _validate_source_id(expected_sections, active_chunk_ids)

            if validate_output == SECTION_EMPTY:
                print(f"Empty expected sections for {question_json["id"]} in line number: {line_number}")
                continue
            elif validate_output == UNSUPPORTED_SOURCE_ID:
                print(f"Unsupported source id in expected sections for {question_json["id"]} in line number: {line_number}")
                continue

if __name__ == "__main__":
    validate_search_cases()
def normalize_subject(text: str) -> str:
    return " ".join(text.split())




"""
validate_ticket(record:dict)
string id, subject, body - dictionary - validate string and body maybe empty
unknown fields are rejected
return a clean ticket or raise a ValueError 
check input is dict before indexing it
"""

REQUIRED_FIELDS = ("id", "subject", "body")
NON_BLANK_FIELDS = ("id", "subject")

def validate_ticket(record:dict) -> dict:
    if type(record) is not dict:
        raise ValueError(f"Ticket must be in dictionary, got {type(record).__name__}")
    
    invalid_keys = []
    for key in record:
        if key not in REQUIRED_FIELDS:
            invalid_keys.append(key)
            
    if len(invalid_keys) > 0:
        raise ValueError(f"Missing field(s): '{', '.join(invalid_keys)}'")
    
    cleaned_ticket:dict = {
        "id": record['id'].strip(),
        "subject": record['subject'].strip(),
        "body": record['body'].strip()
    }
    
    for k in NON_BLANK_FIELDS:
        if not cleaned_ticket[k]:
            raise ValueError("Field {k} must not be blank")
    
    return cleaned_ticket
    




"""
A user needs to find and repair the bad records.
Read tickets from path (UTF-8)
Record line and reason for each rejection; explicitly reject blank lines
Catch JSON parse errors and validation errors separately
"""

import json
import sys

def read_tickets() -> list:
    path = sys.argv[1]
    ticket_ids:set = set()
    cleaned_ticket:list = []
    
    with open(path, 'r', encoding='utf-8') as ticket_file:
        count = 0
        for line_number, line in enumerate(ticket_file, start=1):
            count += 1
            if line.strip():
                try:
                    ticket = json.loads(line)
                    
                    if ticket["id"]:
                        ticket_ids.add(ticket['id'])
                        cleaned_ticket.append(ticket)
                    else:
                        raise ValueError("Invalid JSON. Missing id in ticket")
                except json.JSONDecodeError as e:
                    print(f"Line {line_number} [JSON Syntax Error]: {e.msg}", file=sys.stderr)
                except (ValueError, KeyError) as e:
                    print(f"Line {line_number} [Validation Error]: {e} ", file=sys.stderr)
            else:
                print(f"Skipping empty line number: {line_number}")
                
        print(f"Scanned {count} total item(s) from file.")    
    return cleaned_ticket
                
                


"""
A user needs to find and repair the bad records.
Read tickets from path (UTF-8)
Record line and reason for each rejection; explicitly reject blank lines
Catch JSON parse errors and validation errors separately

Addons
Add --out-dir.
(clean.jsonl and rejected.jsonl)
Run python -m ticket_doctor fixtures/tickets_dirty.jsonl --out-dir out/tickets.

Keep accepted rows in input order.
Include original line number and reason for rejections; don't copy the ticket body into diagnostics.
"""

# Building output directory for tickets after read
def build_out_dir() -> str:
    output_action = sys.argv[2]
    output_path = sys.argv[3]
    
    print(output_path)
    
    if output_action == "--out-dir":
        path = Path(f"{output_path}")
        path.mkdir(parents=True, exist_ok=True)
        return SKIP_OUT_DIR_FALSE
    else:
        return SKIP_OUT_DIR
    

import json
import sys
from pathlib import Path

SKIP_OUT_DIR = "SKIP_OUT_DIR"
SKIP_OUT_DIR_FALSE = "SKIP_OUT_DIR_FALSE"

CLEAN_TICKET_FILE_NAME = "clean.jsonl"
REJECTED_TICKET_FILE_NAME = "rejected.jsonl"

def build_clean_tickets() -> None:
    should_skip_writeable_output = build_out_dir() == SKIP_OUT_DIR
    
    cleaned_tickets = []
    rejected_tickets = []
    accepted_ticket_ids = set()
    
    ticket_path = sys.argv[1]
    
    if not ticket_path:
        print("Invalid path given to read ticket(s)")
        sys.exit()
        
    with open(ticket_path, encoding='UTF-8', mode='r') as ticket_file:
        for line_number, line in enumerate(ticket_file, start=1):  # start=1 is counter starts from 1
            print(f"Scanning line number {line_number}")
            
            if not line:
                print(f"[Empty Line]. Skipping line number {line_number}.")
            
            try:
                ticket = json.loads(line)
                ticket_id = ticket["id"].strip()
                
                if not ticket_id:
                    raise ValueError(f"Missing ticket id in line number {line_number}")
                if ticket_id in accepted_ticket_ids:
                    raise ValueError(f"Duplicate ids found. Skipping line number {line_number}")
                
                accepted_ticket_ids.add(ticket_id.strip())
                cleaned_tickets.append(ticket)
                
            except json.JSONDecodeError as e:
                rejected_tickets.append(line)
                print(f"[JSON Parse Error]. Error in line {line_number}. Message: {e.msg}")
            except (ValueError, KeyError) as e:
                rejected_tickets.append(line)
                print(f"[Value/Key Error]. Error in line {line_number}. Message: {e}")
    
    if not should_skip_writeable_output:
        clean_full_path = Path(f"{sys.argv[3]}/{CLEAN_TICKET_FILE_NAME}")
        rejected_full_path = Path(f"{sys.argv[3]}/{REJECTED_TICKET_FILE_NAME}")
        print(clean_full_path)
        
        with(
            clean_full_path.open("w", encoding="UTF-8") as clean_tickets_writeable_file,
            rejected_full_path.open("w", encoding="UTF-8") as rejected_tickets_writeable_file
        ):
            for clean in cleaned_tickets:
                clean_tickets_writeable_file.write(json.dumps(clean) + "\n")
            
            for reject in rejected_tickets:
                rejected_tickets_writeable_file.write(json.dumps(reject) + "\n")


if __name__ == "__main__":
    build_clean_tickets()
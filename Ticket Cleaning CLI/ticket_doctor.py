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

def read_tickets(path:str) -> list:
    ticket_ids:set = set()
    cleaned_ticket:list = []
    
    with open(path, 'r', encoding='utf-8') as ticket_file:
        for line_number, line in enumerate(ticket_file, start=1):
            if line.strip():
                try:
                    ticket = json.loads(line)
                    
                    if ticket["id"]:
                        ticket_ids.add(ticket['id'])
                        cleaned_ticket.append(ticket)
                    else:
                        raise ValueError("Invalid JSON. Missing id in ticket")
                except json.JSONDecodeError as e:
                    print(f"Line {line_number} [JSON Syntax Error]: {e.msg}")
                except (ValueError, KeyError) as e:
                    print(f"Line {line_number} [Validation Error]: {e} ")
                
            else:
                print(f"Skipping empty line number: {line_number}")
    return cleaned_ticket
                
                


if __name__ == "__main__":
    tickets = read_tickets('./fixtures/tickets_dirty.jsonl')
    print(tickets)

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

def validate_ticket(record:dict):
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
    
    

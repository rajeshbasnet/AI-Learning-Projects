"""
RECAP WEEK 1 KNOWLEDGE BASE

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

import json
import sys

from pathlib import Path

CLEAN_TICKETS_FILENAME = "clean.jsonl"
REJECTED_TICKETS_FILENAME = "rejected.jsonl"

def read_tickets() -> None:
    dirty_ticket_path =  Path(sys.argv[1])
    should_write_to_output_dir = sys.argv[2] == "--out-dir"
    
    if not should_write_to_output_dir:
        raise ValueError(f"[--out-dir] Output directory action missing")
        
    output_dir = sys.argv[3]
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)
    

    clean_json_output_full_path = Path(f"{output_dir}/{CLEAN_TICKETS_FILENAME}")
    rejected_json_output_full_path = Path(f"{output_dir}/{REJECTED_TICKETS_FILENAME}")
    
    with(
        dirty_ticket_path.open("r", encoding="UTF-8") as dirty_tickets_file,
        clean_json_output_full_path.open("w", encoding="UTF-8") as clean_json_output_file,
        rejected_json_output_full_path.open("w", encoding="UTF-8") as rejected_json_output_file,
    ):
        for line_number, line in enumerate(dirty_tickets_file, start=1):
            try:
                print(f"Processing line number {line_number}")
                
                line = line.strip()
                if not line:
                    print(f"Skipping line number {line_number} due to empty\n")
                    continue
                
                ticket:dict = json.loads(line)
                ticket_id = ticket['id'].strip()
                
                if not ticket_id:
                    raise ValueError(f"Ticket id missing for line number {line_number}")
                
                cleaned_ticket = json.dumps(ticket)
                clean_json_output_file.write(f"{cleaned_ticket} \n")
            except json.JSONDecodeError as e:
                rejected_json_output_file.write(f"{line}  Reason:{e.msg} \n")
            except (ValueError, KeyError) as e:
                rejected_json_output_file.write(f"{line}  Reason:{e} \n")
            print(f"Completed task for line number {line_number} \n")
        
        
    
    
    
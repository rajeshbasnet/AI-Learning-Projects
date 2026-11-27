"""
TicketExtraction(BaseModel)
category: Literal["billing", "access", "bug", "unknown"] - ticket
error_code: optional string
summary: string
missing info: list string

it's methods:
model_validate_json(str) - it has it's own method
"""

from pydantic import BaseModel
from typing import Literal, Any
from typing import Optional

import httpx

from ticket_extractor.model_client import post_chat
from ticket_extractor.local_chat import LOCAL_URL

class TicketExtraction(BaseModel):
    category: Literal["billing", "access", "bug", "unknown"]
    error_code: Optional[str] = None
    summary: str
    missing_info: list[str]


TicketExtraction.model_validate_json('{"category":"bug","error_code":"EXP-104","summary":"Export failed.","missing_info":[]}')
# TicketExtraction.model_validate_json(
# '{"category":"urgent","error_code":"EXP-104","summary":"Export failed.","missing_info":[]}'
# ) # raises ValidationError
_format_schema:Optional[dict[str, Any]] = TicketExtraction.model_json_schema()


DEFAULT_PROMPT:str = """
Classify the ticket as billing, access, bug, or unknown. 
Use billing for invoice/payment issues, access for account/sign-in issues, 
and bug for product failures. Use unknown if the ticket does not support a label. 
Copy error_code only when an explicit code appears. Do not invent details. 
Return summary and missing_info as strings/lists that match the schema."

Ticket: {ticket_text}
"""

def build_prompt(template:str, ticket_text:str) -> str:
    return template.replace("{ticket_text}", ticket_text)

def extract_ticket(
        client:httpx.Client,
        ticket_text:str,
        model:str = "qwen3.5:4b",
        prompt_template:str = DEFAULT_PROMPT) -> None:
    # build prompt
    prompt:str = build_prompt(prompt_template, ticket_text)

    # validate format schema
    response = post_chat(client=client, prompt=prompt, model=model, format_schema=_format_schema)
    print(TicketExtraction.model_validate_json(response))



if __name__ == "__main__":
    _client = httpx.Client(base_url=LOCAL_URL)
    _ticket_text = "Export failed with EXP-104."
    extract_ticket(client=_client, ticket_text=_ticket_text)
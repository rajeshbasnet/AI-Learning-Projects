from typing import Any, Optional

import httpx
from httpx import Client
from ticket_extractor.local_chat import LOCAL_URL, MessageRequest, ChatMessage

"""
method - post_chat(client, prompt, model)
Reject blank value
Return data["message"]["content"] only when it is a string; 
otherwise raise ResponseShapeError, a ValueError subclass for a missing or wrongly typed response field.
"""

class ResponseShapeError(ValueError):
    pass

def post_chat(
        client: Client,
        prompt: str,
        model: str = "qwen3.5:4b",
        format_schema: Optional[dict[str, Any]] = None ) -> str:
    if not prompt:
        raise ValueError("Missing prompt value")

    chat_messages: ChatMessage = ChatMessage(
        role="user",
        content=prompt
    )

    message_request = MessageRequest(
        model=model,
        messages=[chat_messages],
        think=False,
        stream=False,
        format = format_schema
    )

    with client as c:
        try:
            url = LOCAL_URL
            body = message_request

            response = c.post(url=url, json=body)
            response.raise_for_status()
            content =  response.json()

            if type(content["message"]["content"]) is not str:
                raise ResponseShapeError("[Type Mismatch] Content retrieved from response is not in string")

            return content["message"]["content"]

        except httpx.ConnectError as e:
            raise RuntimeError("Could not connect. Is the server running?")
        except httpx.TimeoutException as e:
            raise TimeoutError("Request timeout.") from e
        except httpx.RequestError as e:
            raise RuntimeError(f"Ollama returned HTTP Code: {response.status_code}") from e
        except ValueError as e:
            raise ValueError(f"[Value Error]. Exception: {e}")

if __name__ == "__main__":
    _client = httpx.Client()
    print(post_chat(client=_client, prompt="Hey", format_schema=None))

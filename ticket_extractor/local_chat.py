import json
from argparse import ArgumentParser
import urllib
import urllib.error


from typing import *
from urllib.request import Request

LOCAL_URL = "http://127.0.0.1:11434/api/chat"

class ChatMessage(TypedDict):
    role:str
    content:str


class ChatResponse(TypedDict):
    model:str
    message:ChatMessage
    done:bool
    prompt_eval_count: int
    eval_count:int

class MessageRequest(TypedDict):
    model:str
    messages:list[ChatMessage]
    think:bool
    stream:bool
    format:Optional[dict[str,Any]]

"""
localhost:11434/api/chat - send a request to model
send_chat - method name - include timeout_seconds
reject blank prompt and timeout_seconds <= 0 with ValueError
validate response object and every field exact type
python treats bool value as int e.g. False == 0 and True == 1 so check exact type
"""
def send_chat(model:str, prompt:str, timeout_seconds:float) -> ChatResponse:
    if not prompt:
        raise ValueError("[Invalid Request] Missing prompt value")

    chat_messages = ChatMessage(
        role="user",
        content=prompt
    )
    message_request = MessageRequest(
        model=model,
        messages=[chat_messages],
        think=False,
        stream=False
    )

    request = Request(
        url=LOCAL_URL,
        data=json.dumps(message_request).encode("utf-8"),
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            data:ChatResponse = json.loads(response.read().decode("utf-8"))
            return data
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Ollama returned HTTP Code: {e.code}: {e.read().decode()}")
    except urllib.error.URLError as e:
        raise RuntimeError("Can't reach Ollama. Is it running? Try: ollama serve") from e
    except TimeoutError as e:
        raise RuntimeError(f"No reply within {timeout_seconds}s") from e


def main() -> None:
    parser = ArgumentParser(description="Chat to ollama via Python builtin method")
    parser.add_argument("prompt", type=str, help="Text to send to Ollama")
    parser.add_argument("--model", help="Ollama model tag", default="qwen3.5:4b")
    parser.add_argument("--timeout", help="Request timeout in seconds (default: 120)", default=120)

    args = parser.parse_args()

    prompt = args.prompt
    model = args.model
    timeout = args.timeout

    send_chat(model, prompt, timeout)


if __name__ == "__main__":
    main()
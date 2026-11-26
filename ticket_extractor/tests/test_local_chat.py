from ticket_extractor.local_chat import send_chat

short = send_chat(model="qwen3.5:4b", prompt="Summarize: Export failed with EXP-104.", timeout_seconds=120)
long = send_chat(
    model="qwen3.5:4b",
    prompt="Summarize: Export failed with EXP-104. The customer retried twice "
    "this morning and says the download stops at 52 MB.",
    timeout_seconds=120
)

print("short prompt tokens:", short["prompt_eval_count"])
print("long prompt tokens:", long["prompt_eval_count"])
print("short output tokens:", short["eval_count"])
print("long output tokens:", long["eval_count"])
assert long["prompt_eval_count"] > short["prompt_eval_count"]
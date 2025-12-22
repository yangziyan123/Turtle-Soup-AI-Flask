import os

from volcenginesdkarkruntime import Ark

client = Ark(api_key=os.environ.get("ARK_API_KEY"))

if __name__ == "__main__":
    resp = client.chat.completions.create(
        model="doubao-seed-1-6-251015",
        messages=[{"content":"You are a helpful assistant.","role":"system"},{"content":"hello","role":"user"}],
        stream=True,
    )
    for chunk in resp:
        if not chunk.choices:
            continue

        print(chunk.choices[0].delta.content, end="")
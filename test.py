from groq import Groq

client = Groq(api_key="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")

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",  # ← changed this line
    messages=[{"role": "user", "content": "Say hello in one sentence!"}]
)

print(response.choices[0].message.content)
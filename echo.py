import openai
openai.api_key = "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"

def chatbot(prompt):
  response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
  )

  return response["choices"][0]["text"]

print(chatbot("Hello, how are you today?"))

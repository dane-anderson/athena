from models.ollama_client import OllamaClient


client = OllamaClient()

response = client.generate(
    "Say hello and introduce yourself as Athena.",
    "qwen3.5:122b"
)

print(response)
# core/mistral_prompt.py
import subprocess
import json

def ask_mistral(prompt: str) -> str:
    command = ["ollama", "run", "mistral"]
    result = subprocess.run(command, input=prompt.encode(), capture_output=True)
    return result.stdout.decode()

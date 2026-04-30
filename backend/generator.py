import json
from llm import chat_json

def generate_code(requirement: str) -> dict:
    prompt = f"""
Generate Python code based on the requirement. Return JSON with filename as key and code as value.
Requirement: {requirement}
"""
    return chat_json(prompt, "You are a Python developer. Return only JSON.")

def generate_tests(files: dict) -> dict:
    prompt = f"""
Generate pytest test code for the following files. Return JSON with test filename as key and code as value.
Files: {json.dumps(files, indent=2)}
"""
    return chat_json(prompt, "You are a Python test engineer. Return only JSON.")

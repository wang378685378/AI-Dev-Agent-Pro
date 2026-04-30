import json
from llm import chat_json
from typing import Dict

class CodeAgent:
    def generate(self, requirement: str) -> Dict[str, str]:
        prompt = f"""
Generate Python code based on the requirement. Return JSON with filename as key and code as value.
Requirement: {requirement}
"""
        return chat_json(prompt, "You are a Python developer. Return only valid JSON.")

class TestAgent:
    def generate(self, files: Dict[str, str]) -> Dict[str, str]:
        prompt = f"""
Generate pytest test code for the following files. Return JSON with test filename as key and code as value.
Files: {json.dumps(files, indent=2)}
"""
        return chat_json(prompt, "You are a Python test engineer. Return only valid JSON.")

class FixAgent:
    def fix(self, files: Dict[str, str], tests: Dict[str, str], error_log: str) -> Dict[str, str]:
        prompt = f"""
Fix the following code based on test failures. Return JSON with corrected filename as key and code as value.
Files: {json.dumps(files, indent=2)}
Tests: {json.dumps(tests, indent=2)}
Error (last 2000 chars): {error_log[-2000:]}
"""
        return chat_json(prompt, "You are a Python developer. Fix the code. Return only valid JSON.")

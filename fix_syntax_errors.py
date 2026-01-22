#!/usr/bin/env python3
"""Fix syntax errors in voice_synthesis.py"""
import re

file_path = "src/services/voice_synthesis.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix escaped quotes
content = content.replace("if hasattr(self.engine, \\'delete_voice\\'):", "if hasattr(self.engine, 'delete_voice'):")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed syntax error in voice_synthesis.py")

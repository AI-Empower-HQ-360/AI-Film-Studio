"""
Cline AI Extension Test File
Use this file to test Cline's code generation capabilities

Instructions:
1. Place your cursor on a TODO comment
2. Ask Cline to generate the code (usually Ctrl+Space or Tab)
3. Review the generated code
4. Test if it works correctly
"""

# ==================== Test 1: Function Generation ====================

# TODO: Generate a function to validate email addresses
# Expected: Cline should generate a function with email validation logic

# TODO: Generate a function to create a character with validation
# Expected: Cline should generate a function that creates a Character object

# TODO: Generate a pytest test function for the Character Engine
# Expected: Cline should generate a test function with proper fixtures

# ==================== Test 2: Code Explanation ====================

# Select the code below and ask Cline to explain it
def complex_function(data: dict) -> list:
    """Complex function for Cline to explain"""
    result = []
    for key, value in data.items():
        if isinstance(value, (list, dict)):
            result.extend([f"{key}:{item}" for item in (value if isinstance(value, list) else value.items())])
        else:
            result.append(f"{key}:{value}")
    return sorted(result, key=len, reverse=True)

# ==================== Test 3: Code Refactoring ====================

# Select the code below and ask Cline to refactor it
def old_style_function(x, y, z):
    result = []
    for i in range(x):
        temp = []
        for j in range(y):
            if i % 2 == 0 and j % 2 == 0:
                temp.append(i * j + z)
        result.append(temp)
    return result

# ==================== Test 4: Type Hints ====================

# TODO: Add type hints to this function
def untyped_function(data, options):
    result = {}
    for key in data:
        if key in options:
            result[key] = data[key] * options[key]
    return result

# ==================== Test 5: Error Handling ====================

# TODO: Add error handling to this function
def unsafe_function(url):
    import requests
    response = requests.get(url)
    return response.json()

# ==================== Test 6: Documentation ====================

# TODO: Generate docstring for this function
def undocumented_function(character_id: str, scene_id: str) -> dict:
    from src.engines.character_engine import CharacterEngine
    engine = CharacterEngine()
    character = engine.get_character(character_id)
    return {"character": character, "scene": scene_id}

# ==================== Test 7: Test Generation ====================

# TODO: Generate a pytest test for the function above
# Expected: Cline should generate a complete test with mocks

# ==================== Test 8: Async Function ====================

# TODO: Convert this to an async function
def sync_function():
    import time
    time.sleep(1)
    return "done"

# ==================== Test 9: Class Generation ====================

# TODO: Generate a class for managing video projects
# Expected: Cline should generate a class with methods for project management

# ==================== Test 10: Integration ====================

# TODO: Generate code that integrates Character Engine with Writing Engine
# Expected: Cline should understand both engines and create integration code

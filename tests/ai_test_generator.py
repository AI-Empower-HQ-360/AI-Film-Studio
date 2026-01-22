"""
AI-powered test generator using OpenAI GPT-4
Analyzes source code and generates comprehensive test suites
"""
import os
import ast
import argparse
from typing import List, Dict, Any
from pathlib import Path

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: openai package not installed. Install with: pip install openai")


class AITestGenerator:
    """Generate tests using AI"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if OPENAI_AVAILABLE and self.api_key:
            openai.api_key = self.api_key
    
    def analyze_function(self, source_code: str) -> Dict[str, Any]:
        """Analyze function to extract metadata"""
        tree = ast.parse(source_code)
        
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    "name": node.name,
                    "args": [arg.arg for arg in node.args.args],
                    "returns": ast.unparse(node.returns) if node.returns else None,
                    "is_async": isinstance(node, ast.AsyncFunctionDef)
                })
        
        return {"functions": functions}
    
    def generate_test_prompt(self, source_code: str, context: str = "") -> str:
        """Generate prompt for AI test generation"""
        prompt = f"""
You are an expert Python test engineer. Generate comprehensive pytest tests for the following code.

{f"Context: {context}" if context else ""}

Source Code:
```python
{source_code}
```

Generate tests that include:
1. Happy path tests (normal usage)
2. Edge cases (empty inputs, None values, boundary conditions)
3. Error handling tests (invalid inputs, exceptions)
4. Mock external dependencies (APIs, databases, S3)
5. Async tests if the code is async
6. Fixtures for common setup

Requirements:
- Use pytest framework
- Use @pytest.mark.asyncio for async tests
- Mock external services (boto3, requests, OpenAI API)
- Include docstrings for each test
- Use descriptive test names starting with test_
- Add appropriate assertions

Return ONLY the test code, no explanations.
"""
        return prompt
    
    def generate_tests(self, source_code: str, context: str = "") -> str:
        """Generate tests using GPT-4"""
        if not OPENAI_AVAILABLE:
            return "# Error: OpenAI package not installed"
        
        if not self.api_key:
            return "# Error: OPENAI_API_KEY not set"
        
        prompt = self.generate_test_prompt(source_code, context)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert Python test engineer specializing in pytest."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"# Error generating tests: {str(e)}"
    
    def generate_tests_for_file(self, file_path: str) -> str:
        """Generate tests for an entire file"""
        with open(file_path, 'r') as f:
            source_code = f.read()
        
        file_name = Path(file_path).stem
        context = f"This is from {file_name}.py in the AI Film Studio project"
        
        return self.generate_tests(source_code, context)
    
    def save_tests(self, test_code: str, output_path: str):
        """Save generated tests to file"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(test_code)
        
        print(f"✅ Tests saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="AI-powered test generator")
    parser.add_argument("input_file", help="Path to Python file to generate tests for")
    parser.add_argument("--output", "-o", help="Output path for generated tests")
    parser.add_argument("--api-key", help="OpenAI API key (or set OPENAI_API_KEY env var)")
    parser.add_argument("--print-only", action="store_true", help="Print tests without saving")
    
    args = parser.parse_args()
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        input_path = Path(args.input_file)
        output_path = f"tests/test_{input_path.stem}.py"
    
    # Generate tests
    generator = AITestGenerator(api_key=args.api_key)
    
    print(f"🤖 Generating tests for {args.input_file}...")
    test_code = generator.generate_tests_for_file(args.input_file)
    
    if args.print_only:
        print("\n" + "="*50)
        print(test_code)
        print("="*50)
    else:
        generator.save_tests(test_code, output_path)
        print(f"📝 Review the generated tests at {output_path}")
        print("💡 Tip: Always review and adjust AI-generated tests before using them!")


if __name__ == "__main__":
    main()

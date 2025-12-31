"""Setup configuration for AI Film Studio"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-film-studio",
    version="0.1.0",
    author="AI Empower HQ 360",
    description="AI-powered film production tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="backend") + find_packages(where="ai"),
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "torch>=2.0.0",
        "transformers>=4.35.0",
    ],
)

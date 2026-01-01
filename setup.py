"""Setup configuration for AI Film Studio"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-film-studio",
    version="0.1.0",
    author="AI Empower HQ 360",
    author_email="contact@ai-empower-hq.com",
    description="AI-powered film production tools for creating cinematic short films from text scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AI-Empower-HQ-360/AI-Film-Studio",
    project_urls={
        "Bug Reports": "https://github.com/AI-Empower-HQ-360/AI-Film-Studio/issues",
        "Source": "https://github.com/AI-Empower-HQ-360/AI-Film-Studio",
        "Documentation": "https://github.com/AI-Empower-HQ-360/AI-Film-Studio/tree/main/docs",
    },
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "torch>=2.0.0",
        "transformers>=4.35.0",
    ],
    classifiers=[
        # Development Status
        "Development Status :: 3 - Alpha",
        
        # Intended Audience
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        
        # Topic Tags
        "Topic :: Multimedia :: Video",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        
        # License
        "License :: OSI Approved :: MIT License",
        
        # Python Version Support
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        
        # Operating Systems
        "Operating System :: OS Independent",
        
        # Framework
        "Framework :: FastAPI",
        
        # Environment
        "Environment :: Web Environment",
        "Environment :: GPU",
    ],
    keywords=[
        "ai",
        "film",
        "video-generation",
        "machine-learning",
        "computer-vision",
        "stable-diffusion",
        "fastapi",
        "cloud-native",
        "aws",
        "devops",
        "mlops",
    ],
    license="MIT",
)

"""
Setup script for crossword-generator package
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="crossword-generator",
    version="0.1.0",
    description="A Python-based crossword puzzle generator using CSP techniques",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/crossword-generator",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        # Add dependencies from requirements.txt here
    ],
    entry_points={
        "console_scripts": [
            "crossword-generate=scripts.generate:main",
            "crossword-download=scripts.download_wordlist:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)


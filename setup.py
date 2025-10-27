"""Setup configuration for Claude Codex."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "CLAUDE_CODEX_README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="claude-codex",
    version="0.1.0",
    author="Dennis Kidwell",
    author_email="",
    description="AI-powered code intelligence using Claude by Anthropic - like OpenAI Codex but for Claude",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dkid713/Dennis-Kidwell",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "anthropic>=0.40.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "isort>=5.10.0",
            "mypy>=0.990",
            "flake8>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "claude-codex=claude_codex.cli:main",
            "claude-chat=claude_codex.interactive:main",
            "claude-tutor=claude_codex.tutor:main",
        ],
    },
    keywords="claude anthropic codex ai code-generation code-analysis llm",
    project_urls={
        "Bug Reports": "https://github.com/Dkid713/Dennis-Kidwell/issues",
        "Source": "https://github.com/Dkid713/Dennis-Kidwell",
    },
)

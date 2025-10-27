"""
Claude Codex - An AI-powered code understanding and generation system using Claude by Anthropic.

This library provides a comprehensive interface for leveraging Claude's capabilities
for software development tasks including code generation, explanation, debugging,
refactoring, and more.
"""

from .client import ClaudeCodex
from .types import (
    CodexResponse,
    CodeGenerationRequest,
    CodeExplanationRequest,
    CodeReviewRequest,
    DebuggingRequest,
    RefactoringRequest,
)

__version__ = "0.1.0"
__all__ = [
    "ClaudeCodex",
    "CodexResponse",
    "CodeGenerationRequest",
    "CodeExplanationRequest",
    "CodeReviewRequest",
    "DebuggingRequest",
    "RefactoringRequest",
]

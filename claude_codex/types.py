"""Type definitions for Claude Codex."""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum


class Language(str, Enum):
    """Supported programming languages."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CPP = "cpp"
    CSHARP = "csharp"
    GO = "go"
    RUST = "rust"
    RUBY = "ruby"
    PHP = "php"
    SWIFT = "swift"
    KOTLIN = "kotlin"
    SQL = "sql"
    HTML = "html"
    CSS = "css"
    SHELL = "shell"
    AUTO = "auto"


class CodexMode(str, Enum):
    """Different modes of operation for Claude Codex."""
    GENERATE = "generate"
    EXPLAIN = "explain"
    REVIEW = "review"
    DEBUG = "debug"
    REFACTOR = "refactor"
    COMPLETE = "complete"
    DOCUMENT = "document"
    TRANSLATE = "translate"
    TEST = "test"


@dataclass
class CodexResponse:
    """Response from Claude Codex operations."""
    content: str
    mode: CodexMode
    language: Optional[Language] = None
    metadata: Optional[Dict[str, Any]] = None
    tokens_used: Optional[int] = None


@dataclass
class CodeGenerationRequest:
    """Request for code generation."""
    description: str
    language: Language
    context: Optional[str] = None
    examples: Optional[List[str]] = None
    constraints: Optional[List[str]] = None
    style_guide: Optional[str] = None


@dataclass
class CodeExplanationRequest:
    """Request for code explanation."""
    code: str
    language: Language = Language.AUTO
    detail_level: str = "medium"  # low, medium, high
    focus_areas: Optional[List[str]] = None


@dataclass
class CodeReviewRequest:
    """Request for code review."""
    code: str
    language: Language = Language.AUTO
    review_aspects: Optional[List[str]] = None  # security, performance, style, etc.
    severity_threshold: str = "all"  # all, warning, error


@dataclass
class DebuggingRequest:
    """Request for debugging assistance."""
    code: str
    error_message: Optional[str] = None
    expected_behavior: Optional[str] = None
    language: Language = Language.AUTO
    context: Optional[str] = None


@dataclass
class RefactoringRequest:
    """Request for code refactoring."""
    code: str
    language: Language = Language.AUTO
    goals: List[str] = None  # readability, performance, maintainability, etc.
    constraints: Optional[List[str]] = None

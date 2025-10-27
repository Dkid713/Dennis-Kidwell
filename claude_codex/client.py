"""Main Claude Codex client implementation."""

import os
from typing import Optional, List, Dict, Any
from anthropic import Anthropic

from .types import (
    CodexResponse,
    CodexMode,
    Language,
    CodeGenerationRequest,
    CodeExplanationRequest,
    CodeReviewRequest,
    DebuggingRequest,
    RefactoringRequest,
)


class ClaudeCodex:
    """
    Claude Codex - AI-powered code intelligence using Claude by Anthropic.

    This class provides a comprehensive interface for leveraging Claude's capabilities
    in software development workflows including code generation, understanding,
    debugging, and more.

    Example:
        >>> codex = ClaudeCodex(api_key="your-api-key")
        >>> response = codex.generate_code(
        ...     description="Create a function to calculate fibonacci numbers",
        ...     language=Language.PYTHON
        ... )
        >>> print(response.content)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 4096,
        temperature: float = 0.3,
    ):
        """
        Initialize Claude Codex client.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            model: Claude model to use
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0.0-1.0)
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set in ANTHROPIC_API_KEY environment variable")

        self.client = Anthropic(api_key=self.api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

    def _call_claude(
        self,
        system_prompt: str,
        user_message: str,
        temperature: Optional[float] = None,
    ) -> tuple[str, int]:
        """Internal method to call Claude API."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=temperature or self.temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )

        content = response.content[0].text
        tokens_used = response.usage.input_tokens + response.usage.output_tokens

        return content, tokens_used

    def generate_code(
        self,
        description: str,
        language: Language,
        context: Optional[str] = None,
        examples: Optional[List[str]] = None,
        constraints: Optional[List[str]] = None,
        style_guide: Optional[str] = None,
    ) -> CodexResponse:
        """
        Generate code based on natural language description.

        Args:
            description: Natural language description of what to generate
            language: Target programming language
            context: Additional context about the codebase or requirements
            examples: Example code snippets for reference
            constraints: List of constraints or requirements
            style_guide: Coding style guidelines to follow

        Returns:
            CodexResponse with generated code
        """
        system_prompt = f"""You are Claude Codex, an expert programming assistant specializing in {language.value} development.
Your task is to generate high-quality, production-ready code based on user requirements.

Guidelines:
- Write clean, efficient, and well-documented code
- Follow {language.value} best practices and idioms
- Include appropriate error handling
- Add helpful comments for complex logic
- Consider edge cases and input validation"""

        if style_guide:
            system_prompt += f"\n- Follow this style guide: {style_guide}"

        user_message = f"Generate {language.value} code for: {description}"

        if context:
            user_message += f"\n\nContext: {context}"

        if constraints:
            user_message += f"\n\nConstraints:\n" + "\n".join(f"- {c}" for c in constraints)

        if examples:
            user_message += f"\n\nReference examples:\n" + "\n\n".join(examples)

        content, tokens = self._call_claude(system_prompt, user_message)

        return CodexResponse(
            content=content,
            mode=CodexMode.GENERATE,
            language=language,
            tokens_used=tokens,
        )

    def explain_code(
        self,
        code: str,
        language: Language = Language.AUTO,
        detail_level: str = "medium",
        focus_areas: Optional[List[str]] = None,
    ) -> CodexResponse:
        """
        Explain what code does in natural language.

        Args:
            code: The code to explain
            language: Programming language (auto-detect if not specified)
            detail_level: Level of detail (low, medium, high)
            focus_areas: Specific aspects to focus on

        Returns:
            CodexResponse with code explanation
        """
        system_prompt = """You are Claude Codex, an expert at analyzing and explaining code.
Provide clear, accurate explanations that help developers understand code quickly.

Your explanations should:
- Start with a high-level overview
- Break down complex logic into understandable parts
- Explain the purpose and flow of the code
- Highlight important patterns or techniques used
- Note any potential issues or areas of concern"""

        user_message = f"Explain this code"

        if language != Language.AUTO:
            user_message += f" ({language.value})"

        user_message += f" with {detail_level} detail:\n\n```\n{code}\n```"

        if focus_areas:
            user_message += f"\n\nFocus on: {', '.join(focus_areas)}"

        content, tokens = self._call_claude(system_prompt, user_message)

        return CodexResponse(
            content=content,
            mode=CodexMode.EXPLAIN,
            language=language,
            tokens_used=tokens,
        )

    def review_code(
        self,
        code: str,
        language: Language = Language.AUTO,
        review_aspects: Optional[List[str]] = None,
        severity_threshold: str = "all",
    ) -> CodexResponse:
        """
        Perform comprehensive code review.

        Args:
            code: The code to review
            language: Programming language
            review_aspects: Specific aspects to review (security, performance, style, etc.)
            severity_threshold: Minimum severity to report (all, warning, error)

        Returns:
            CodexResponse with review findings
        """
        aspects = review_aspects or ["security", "performance", "style", "bugs", "maintainability"]

        system_prompt = f"""You are Claude Codex, an expert code reviewer with deep knowledge of software engineering best practices.

Review the code for:
{chr(10).join(f'- {aspect.title()}' for aspect in aspects)}

Provide:
1. Summary of overall code quality
2. Specific issues found (categorized by severity: error, warning, info)
3. Concrete recommendations for improvement
4. Positive aspects worth noting

Be thorough but constructive in your feedback."""

        user_message = f"Review this code"

        if language != Language.AUTO:
            user_message += f" ({language.value})"

        user_message += f":\n\n```\n{code}\n```"
        user_message += f"\n\nOnly report issues of severity: {severity_threshold}"

        content, tokens = self._call_claude(system_prompt, user_message, temperature=0.2)

        return CodexResponse(
            content=content,
            mode=CodexMode.REVIEW,
            language=language,
            tokens_used=tokens,
        )

    def debug_code(
        self,
        code: str,
        error_message: Optional[str] = None,
        expected_behavior: Optional[str] = None,
        language: Language = Language.AUTO,
        context: Optional[str] = None,
    ) -> CodexResponse:
        """
        Help debug code and identify issues.

        Args:
            code: The problematic code
            error_message: Error message if available
            expected_behavior: Description of expected behavior
            language: Programming language
            context: Additional context about the environment or setup

        Returns:
            CodexResponse with debugging analysis and solutions
        """
        system_prompt = """You are Claude Codex, an expert debugging assistant.

Analyze the code systematically:
1. Identify the root cause of the issue
2. Explain why the problem occurs
3. Provide step-by-step solution
4. Suggest how to prevent similar issues

Be specific and provide working code fixes."""

        user_message = f"Help debug this code"

        if language != Language.AUTO:
            user_message += f" ({language.value})"

        user_message += f":\n\n```\n{code}\n```"

        if error_message:
            user_message += f"\n\nError message:\n{error_message}"

        if expected_behavior:
            user_message += f"\n\nExpected behavior: {expected_behavior}"

        if context:
            user_message += f"\n\nContext: {context}"

        content, tokens = self._call_claude(system_prompt, user_message)

        return CodexResponse(
            content=content,
            mode=CodexMode.DEBUG,
            language=language,
            tokens_used=tokens,
        )

    def refactor_code(
        self,
        code: str,
        language: Language = Language.AUTO,
        goals: Optional[List[str]] = None,
        constraints: Optional[List[str]] = None,
    ) -> CodexResponse:
        """
        Refactor code to improve quality.

        Args:
            code: The code to refactor
            language: Programming language
            goals: Refactoring goals (readability, performance, maintainability, etc.)
            constraints: Constraints to respect during refactoring

        Returns:
            CodexResponse with refactored code and explanation
        """
        goals = goals or ["readability", "maintainability"]

        system_prompt = f"""You are Claude Codex, an expert at code refactoring.

Refactor the code to improve:
{chr(10).join(f'- {goal.title()}' for goal in goals)}

Ensure:
- Functionality remains exactly the same
- Code is cleaner and more maintainable
- Best practices are followed
- Changes are explained clearly"""

        user_message = f"Refactor this code"

        if language != Language.AUTO:
            user_message += f" ({language.value})"

        user_message += f":\n\n```\n{code}\n```"

        if constraints:
            user_message += f"\n\nConstraints:\n" + "\n".join(f"- {c}" for c in constraints)

        content, tokens = self._call_claude(system_prompt, user_message)

        return CodexResponse(
            content=content,
            mode=CodexMode.REFACTOR,
            language=language,
            tokens_used=tokens,
        )

    def complete_code(
        self,
        code_prefix: str,
        language: Language,
        context: Optional[str] = None,
    ) -> CodexResponse:
        """
        Complete partial code (like autocomplete).

        Args:
            code_prefix: The code written so far
            language: Programming language
            context: Additional context about what's needed

        Returns:
            CodexResponse with code completion
        """
        system_prompt = f"""You are Claude Codex, an expert code completion assistant for {language.value}.

Complete the code naturally based on the context and existing code.
- Maintain the same style and conventions
- Complete only what's needed (don't rewrite existing code)
- Ensure the completion is syntactically correct
- Follow {language.value} best practices"""

        user_message = f"Complete this {language.value} code:\n\n```\n{code_prefix}\n```"

        if context:
            user_message += f"\n\nContext: {context}"

        content, tokens = self._call_claude(system_prompt, user_message, temperature=0.4)

        return CodexResponse(
            content=content,
            mode=CodexMode.COMPLETE,
            language=language,
            tokens_used=tokens,
        )

    def generate_documentation(
        self,
        code: str,
        language: Language = Language.AUTO,
        doc_format: str = "markdown",
    ) -> CodexResponse:
        """
        Generate documentation for code.

        Args:
            code: The code to document
            language: Programming language
            doc_format: Documentation format (markdown, docstring, javadoc, etc.)

        Returns:
            CodexResponse with generated documentation
        """
        system_prompt = f"""You are Claude Codex, an expert technical writer and programmer.

Generate comprehensive, clear documentation that includes:
- Overview and purpose
- Function/class/module descriptions
- Parameter descriptions with types
- Return value descriptions
- Usage examples
- Notes about edge cases or important behaviors

Format: {doc_format}"""

        user_message = f"Generate documentation for this code"

        if language != Language.AUTO:
            user_message += f" ({language.value})"

        user_message += f":\n\n```\n{code}\n```"

        content, tokens = self._call_claude(system_prompt, user_message)

        return CodexResponse(
            content=content,
            mode=CodexMode.DOCUMENT,
            language=language,
            tokens_used=tokens,
        )

    def translate_code(
        self,
        code: str,
        from_language: Language,
        to_language: Language,
        maintain_style: bool = True,
    ) -> CodexResponse:
        """
        Translate code from one language to another.

        Args:
            code: The code to translate
            from_language: Source programming language
            to_language: Target programming language
            maintain_style: Whether to maintain similar style/structure

        Returns:
            CodexResponse with translated code
        """
        system_prompt = f"""You are Claude Codex, an expert in multiple programming languages.

Translate code from {from_language.value} to {to_language.value}:
- Preserve the same functionality
- Use idiomatic {to_language.value} patterns
- Follow {to_language.value} best practices
- Add comments explaining any translation decisions
- Ensure type safety and error handling"""

        if maintain_style:
            system_prompt += f"\n- Maintain similar structure and style where appropriate"

        user_message = f"Translate this {from_language.value} code to {to_language.value}:\n\n```\n{code}\n```"

        content, tokens = self._call_claude(system_prompt, user_message)

        return CodexResponse(
            content=content,
            mode=CodexMode.TRANSLATE,
            language=to_language,
            metadata={"from_language": from_language.value},
            tokens_used=tokens,
        )

    def generate_tests(
        self,
        code: str,
        language: Language,
        test_framework: Optional[str] = None,
        coverage_goals: Optional[List[str]] = None,
    ) -> CodexResponse:
        """
        Generate unit tests for code.

        Args:
            code: The code to test
            language: Programming language
            test_framework: Testing framework to use (pytest, jest, junit, etc.)
            coverage_goals: What to test (edge cases, error handling, etc.)

        Returns:
            CodexResponse with generated tests
        """
        framework_msg = f" using {test_framework}" if test_framework else ""

        system_prompt = f"""You are Claude Codex, an expert in test-driven development and {language.value}.

Generate comprehensive unit tests{framework_msg} that:
- Cover normal cases and edge cases
- Test error handling
- Are clear and maintainable
- Follow testing best practices
- Include descriptive test names and comments"""

        user_message = f"Generate unit tests for this {language.value} code:\n\n```\n{code}\n```"

        if coverage_goals:
            user_message += f"\n\nEnsure tests cover: {', '.join(coverage_goals)}"

        content, tokens = self._call_claude(system_prompt, user_message)

        return CodexResponse(
            content=content,
            mode=CodexMode.TEST,
            language=language,
            metadata={"test_framework": test_framework},
            tokens_used=tokens,
        )

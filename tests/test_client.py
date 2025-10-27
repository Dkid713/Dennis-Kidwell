"""Unit tests for Claude Codex client."""

import pytest
from unittest.mock import Mock, patch
from claude_codex import ClaudeCodex
from claude_codex.types import Language, CodexMode


class TestClaudeCodex:
    """Test suite for ClaudeCodex class."""

    @pytest.fixture
    def mock_anthropic(self):
        """Mock Anthropic client."""
        with patch('claude_codex.client.Anthropic') as mock:
            yield mock

    @pytest.fixture
    def codex(self, mock_anthropic):
        """Create ClaudeCodex instance with mocked client."""
        return ClaudeCodex(api_key="test-key")

    def test_init_with_api_key(self, mock_anthropic):
        """Test initialization with API key."""
        codex = ClaudeCodex(api_key="test-key")
        assert codex.api_key == "test-key"
        mock_anthropic.assert_called_once_with(api_key="test-key")

    def test_init_without_api_key(self):
        """Test initialization without API key raises error."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="API key must be provided"):
                ClaudeCodex()

    def test_generate_code_basic(self, codex, mock_anthropic):
        """Test basic code generation."""
        # Mock response
        mock_response = Mock()
        mock_response.content = [Mock(text="def fibonacci(n): ...")]
        mock_response.usage = Mock(input_tokens=100, output_tokens=50)
        codex.client.messages.create.return_value = mock_response

        response = codex.generate_code(
            description="fibonacci function",
            language=Language.PYTHON
        )

        assert response.content == "def fibonacci(n): ..."
        assert response.mode == CodexMode.GENERATE
        assert response.language == Language.PYTHON
        assert response.tokens_used == 150

    def test_explain_code(self, codex, mock_anthropic):
        """Test code explanation."""
        mock_response = Mock()
        mock_response.content = [Mock(text="This function calculates...")]
        mock_response.usage = Mock(input_tokens=100, output_tokens=50)
        codex.client.messages.create.return_value = mock_response

        response = codex.explain_code(
            code="def test(): pass",
            language=Language.PYTHON
        )

        assert response.mode == CodexMode.EXPLAIN
        assert "This function calculates..." in response.content

    def test_review_code(self, codex, mock_anthropic):
        """Test code review."""
        mock_response = Mock()
        mock_response.content = [Mock(text="Issues found: ...")]
        mock_response.usage = Mock(input_tokens=100, output_tokens=50)
        codex.client.messages.create.return_value = mock_response

        response = codex.review_code(
            code="def test(): pass",
            language=Language.PYTHON,
            review_aspects=["security", "style"]
        )

        assert response.mode == CodexMode.REVIEW
        assert response.tokens_used == 150

    def test_debug_code(self, codex, mock_anthropic):
        """Test debugging."""
        mock_response = Mock()
        mock_response.content = [Mock(text="The bug is caused by...")]
        mock_response.usage = Mock(input_tokens=100, output_tokens=50)
        codex.client.messages.create.return_value = mock_response

        response = codex.debug_code(
            code="def test(): x / 0",
            error_message="ZeroDivisionError",
            language=Language.PYTHON
        )

        assert response.mode == CodexMode.DEBUG

    def test_refactor_code(self, codex, mock_anthropic):
        """Test code refactoring."""
        mock_response = Mock()
        mock_response.content = [Mock(text="def improved_test(): ...")]
        mock_response.usage = Mock(input_tokens=100, output_tokens=50)
        codex.client.messages.create.return_value = mock_response

        response = codex.refactor_code(
            code="def test(): pass",
            language=Language.PYTHON,
            goals=["readability"]
        )

        assert response.mode == CodexMode.REFACTOR

    def test_translate_code(self, codex, mock_anthropic):
        """Test code translation."""
        mock_response = Mock()
        mock_response.content = [Mock(text="def test():\n    pass")]
        mock_response.usage = Mock(input_tokens=100, output_tokens=50)
        codex.client.messages.create.return_value = mock_response

        response = codex.translate_code(
            code="function test() {}",
            from_language=Language.JAVASCRIPT,
            to_language=Language.PYTHON
        )

        assert response.mode == CodexMode.TRANSLATE
        assert response.language == Language.PYTHON
        assert response.metadata["from_language"] == "javascript"

    def test_generate_tests(self, codex, mock_anthropic):
        """Test test generation."""
        mock_response = Mock()
        mock_response.content = [Mock(text="def test_my_function(): ...")]
        mock_response.usage = Mock(input_tokens=100, output_tokens=50)
        codex.client.messages.create.return_value = mock_response

        response = codex.generate_tests(
            code="def my_function(): pass",
            language=Language.PYTHON,
            test_framework="pytest"
        )

        assert response.mode == CodexMode.TEST
        assert response.metadata["test_framework"] == "pytest"

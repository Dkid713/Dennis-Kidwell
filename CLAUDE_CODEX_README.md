# Claude Codex

**AI-powered code intelligence using Claude by Anthropic** - Like OpenAI Codex, but powered by Claude.

Claude Codex is a comprehensive toolkit that leverages Claude's advanced language understanding to help with software development tasks including code generation, explanation, debugging, refactoring, and more.

## 🎓 New! Beginner-Friendly Modes

Perfect for people learning to code:
- **🎓 Tutor Mode** (`claude-tutor`) - Learn programming step-by-step
- **💬 Chat Mode** (`claude-chat`) - Interactive Replit-style coding assistant
- **📚 Easy Start Guide** - See `EASY_START.md` for absolute beginners

**Never coded before? Start here:** `bash start.sh`

## Features

- **Code Generation**: Generate code from natural language descriptions
- **Code Explanation**: Understand complex code with detailed explanations
- **Code Review**: Get comprehensive code reviews covering security, performance, and style
- **Debugging**: Identify and fix bugs with AI assistance
- **Refactoring**: Improve code quality and maintainability
- **Code Completion**: Intelligent code completion and suggestions
- **Documentation**: Automatically generate comprehensive documentation
- **Code Translation**: Translate code between programming languages
- **Test Generation**: Create comprehensive unit tests
- **Multi-language Support**: Python, JavaScript, TypeScript, Java, C++, Go, Rust, and more

## Installation

```bash
# Install from source
pip install -e .

# Or install dependencies only
pip install -r requirements.txt
```

## Quick Start

### Python API

```python
from claude_codex import ClaudeCodex
from claude_codex.types import Language

# Initialize the client
codex = ClaudeCodex(api_key="your-anthropic-api-key")

# Generate code
response = codex.generate_code(
    description="Create a function to calculate fibonacci numbers",
    language=Language.PYTHON
)
print(response.content)

# Explain existing code
code = """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
"""

response = codex.explain_code(code, language=Language.PYTHON)
print(response.content)

# Review code
response = codex.review_code(
    code=code,
    language=Language.PYTHON,
    review_aspects=["security", "performance", "style"]
)
print(response.content)
```

### Command Line Interface

```bash
# Set your API key
export ANTHROPIC_API_KEY="your-api-key"

# Generate code
claude-codex generate "fibonacci function" --language python

# Explain code from file
claude-codex explain --file script.py --detail high

# Review code
claude-codex review --file app.js --aspects security performance

# Debug code with error message
claude-codex debug --file buggy.py --error "ValueError: invalid literal"

# Refactor code
claude-codex refactor --file legacy.py --goals readability performance

# Generate tests
claude-codex test --file mycode.py --language python --framework pytest

# Translate code between languages
claude-codex translate --file script.js --to python

# Generate documentation
claude-codex document --file module.py --format markdown

# Read from stdin
cat mycode.py | claude-codex review -
```

## API Reference

### ClaudeCodex Class

Main client for interacting with Claude Codex.

#### Methods

##### `generate_code(description, language, context=None, examples=None, constraints=None, style_guide=None)`

Generate code from natural language description.

**Parameters:**
- `description` (str): What code to generate
- `language` (Language): Target programming language
- `context` (str, optional): Additional context
- `examples` (list, optional): Example code snippets
- `constraints` (list, optional): Constraints to follow
- `style_guide` (str, optional): Style guide to follow

**Returns:** `CodexResponse` with generated code

##### `explain_code(code, language=AUTO, detail_level="medium", focus_areas=None)`

Explain what code does.

**Parameters:**
- `code` (str): Code to explain
- `language` (Language): Programming language
- `detail_level` (str): "low", "medium", or "high"
- `focus_areas` (list, optional): Specific aspects to focus on

**Returns:** `CodexResponse` with explanation

##### `review_code(code, language=AUTO, review_aspects=None, severity_threshold="all")`

Review code for issues.

**Parameters:**
- `code` (str): Code to review
- `language` (Language): Programming language
- `review_aspects` (list, optional): Aspects to review (security, performance, style, etc.)
- `severity_threshold` (str): "all", "warning", or "error"

**Returns:** `CodexResponse` with review findings

##### `debug_code(code, error_message=None, expected_behavior=None, language=AUTO, context=None)`

Debug problematic code.

**Parameters:**
- `code` (str): Code with issues
- `error_message` (str, optional): Error message if available
- `expected_behavior` (str, optional): What should happen
- `language` (Language): Programming language
- `context` (str, optional): Additional context

**Returns:** `CodexResponse` with debugging analysis

##### `refactor_code(code, language=AUTO, goals=None, constraints=None)`

Refactor code to improve quality.

**Parameters:**
- `code` (str): Code to refactor
- `language` (Language): Programming language
- `goals` (list, optional): Goals like "readability", "performance"
- `constraints` (list, optional): Constraints to respect

**Returns:** `CodexResponse` with refactored code

##### `complete_code(code_prefix, language, context=None)`

Complete partial code.

**Parameters:**
- `code_prefix` (str): Code written so far
- `language` (Language): Programming language
- `context` (str, optional): Additional context

**Returns:** `CodexResponse` with completion

##### `generate_documentation(code, language=AUTO, doc_format="markdown")`

Generate documentation for code.

**Parameters:**
- `code` (str): Code to document
- `language` (Language): Programming language
- `doc_format` (str): Documentation format

**Returns:** `CodexResponse` with documentation

##### `translate_code(code, from_language, to_language, maintain_style=True)`

Translate code between languages.

**Parameters:**
- `code` (str): Code to translate
- `from_language` (Language): Source language
- `to_language` (Language): Target language
- `maintain_style` (bool): Whether to maintain style

**Returns:** `CodexResponse` with translated code

##### `generate_tests(code, language, test_framework=None, coverage_goals=None)`

Generate unit tests.

**Parameters:**
- `code` (str): Code to test
- `language` (Language): Programming language
- `test_framework` (str, optional): Testing framework (pytest, jest, etc.)
- `coverage_goals` (list, optional): What to test

**Returns:** `CodexResponse` with generated tests

## Supported Languages

- Python
- JavaScript
- TypeScript
- Java
- C++
- C#
- Go
- Rust
- Ruby
- PHP
- Swift
- Kotlin
- SQL
- HTML/CSS
- Shell/Bash

## Examples

Check out the `examples/` directory for comprehensive examples:

- `basic_usage.py`: Simple examples of each feature
- `advanced_usage.py`: Advanced patterns and use cases

Run examples:
```bash
python examples/basic_usage.py
python examples/advanced_usage.py
```

## Use Cases

### 1. Code Generation
Generate boilerplate, implement algorithms, create API endpoints, etc.

### 2. Learning & Education
Understand complex algorithms, learn new languages, get explanations of unfamiliar code.

### 3. Code Review Automation
Automated code reviews for pull requests, continuous integration checks.

### 4. Legacy Code Maintenance
Understand and refactor legacy codebases, add documentation, improve code quality.

### 5. Debugging Assistant
Quick debugging help, error explanation, solution suggestions.

### 6. Test Coverage
Automatically generate comprehensive test suites for existing code.

### 7. Code Migration
Translate projects between programming languages or frameworks.

## Configuration

### Environment Variables

- `ANTHROPIC_API_KEY`: Your Anthropic API key (required)

### Client Configuration

```python
codex = ClaudeCodex(
    api_key="your-key",              # API key
    model="claude-sonnet-4-20250514", # Claude model to use
    max_tokens=4096,                  # Maximum response tokens
    temperature=0.3                   # Sampling temperature (0.0-1.0)
)
```

## CLI Reference

### Global Options

- `--api-key`: Anthropic API key
- `--model`: Claude model to use
- `--temperature`: Sampling temperature

### Commands

#### `generate` / `gen`
Generate code from description
```bash
claude-codex generate "description" --language python [--context "..."] [--style "..."]
```

#### `explain`
Explain what code does
```bash
claude-codex explain --file code.py [--language python] [--detail medium]
```

#### `review`
Review code for issues
```bash
claude-codex review --file code.py [--aspects security performance] [--severity all]
```

#### `debug`
Debug problematic code
```bash
claude-codex debug --file buggy.py [--error "..."] [--expected "..."]
```

#### `refactor`
Refactor code
```bash
claude-codex refactor --file code.py [--goals readability performance]
```

#### `complete`
Complete partial code
```bash
claude-codex complete --file partial.py --language python [--context "..."]
```

#### `document` / `doc`
Generate documentation
```bash
claude-codex document --file code.py [--format markdown]
```

#### `translate`
Translate code between languages
```bash
claude-codex translate --file script.js --to python
```

#### `test`
Generate unit tests
```bash
claude-codex test --file code.py --language python [--framework pytest]
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/Dkid713/Dennis-Kidwell.git
cd Dennis-Kidwell

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
# Format code
black claude_codex/

# Sort imports
isort claude_codex/

# Type checking
mypy claude_codex/

# Linting
flake8 claude_codex/
```

## Architecture

Claude Codex is built on top of the Anthropic Python SDK and provides:

1. **Type-safe API**: Comprehensive type definitions for all operations
2. **Flexible Interface**: Both Python API and CLI for different workflows
3. **Mode-based Operations**: Each operation (generate, explain, review, etc.) has specialized prompts
4. **Language-aware**: Automatically detects languages and applies appropriate best practices
5. **Customizable**: Configure models, temperature, and other parameters

## Best Practices

1. **Be Specific**: Provide detailed descriptions for better results
2. **Add Context**: Include relevant context about your project/codebase
3. **Use Examples**: Provide example code when generating new code
4. **Review Output**: Always review generated code before using in production
5. **Iterate**: Use multiple operations (generate → review → refactor) for best results

## Comparison with OpenAI Codex

| Feature | Claude Codex | OpenAI Codex |
|---------|--------------|--------------|
| Code Generation | ✓ | ✓ |
| Code Explanation | ✓ | ✗ |
| Code Review | ✓ | ✗ |
| Debugging | ✓ | ✗ |
| Refactoring | ✓ | ✗ |
| Documentation | ✓ | ✗ |
| Translation | ✓ | ✗ |
| Test Generation | ✓ | ✗ |
| CLI Tool | ✓ | ✗ |
| Context Window | 200K tokens | 8K tokens |

## Limitations

- Requires internet connection to access Claude API
- API usage incurs costs based on Anthropic pricing
- Generated code should be reviewed before production use
- Language detection may not always be accurate
- Performance depends on the selected Claude model

## FAQ

**Q: How much does it cost?**
A: Costs depend on Anthropic's API pricing. See https://www.anthropic.com/pricing

**Q: Which Claude model should I use?**
A: `claude-sonnet-4-20250514` offers the best balance of performance and cost. Use `claude-opus-4` for most complex tasks.

**Q: Can I use this offline?**
A: No, Claude Codex requires internet access to communicate with Anthropic's API.

**Q: Is the generated code production-ready?**
A: Always review and test generated code before using in production.

**Q: Can I customize the prompts?**
A: Currently prompts are built-in, but you can fork and modify the `client.py` file.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

MIT License - see LICENSE file for details

## Support

- GitHub Issues: https://github.com/Dkid713/Dennis-Kidwell/issues
- Anthropic Documentation: https://docs.anthropic.com

## Acknowledgments

Built on top of Claude by Anthropic - https://www.anthropic.com

---

Made with Claude by [@Dkid713](https://github.com/Dkid713)

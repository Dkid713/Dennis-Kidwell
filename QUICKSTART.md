# Claude Codex - Quick Start Guide

Get started with Claude Codex in 5 minutes!

## Installation

```bash
# Install the package
pip install -e .

# Or just install dependencies
pip install -r requirements.txt
```

## Setup

Set your Anthropic API key:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Get your API key from: https://console.anthropic.com/

## Try It Out

### 1. Python API

Create a file `test_codex.py`:

```python
from claude_codex import ClaudeCodex
from claude_codex.types import Language

# Initialize
codex = ClaudeCodex()

# Generate a function
response = codex.generate_code(
    description="Create a function that checks if a number is prime",
    language=Language.PYTHON
)

print(response.content)
```

Run it:
```bash
python test_codex.py
```

### 2. Command Line

```bash
# Generate code
claude-codex generate "a function to reverse a string" --language python

# Explain code
echo "def factorial(n): return 1 if n <= 1 else n * factorial(n-1)" | claude-codex explain -

# Review your code
claude-codex review --file mycode.py --aspects security style

# Debug with error
claude-codex debug --file buggy.py --error "IndexError: list index out of range"
```

### 3. Run Examples

Try the included examples:

```bash
# Basic examples
python examples/basic_usage.py

# Advanced examples
python examples/advanced_usage.py
```

## Common Use Cases

### Generate a REST API Endpoint

```bash
claude-codex generate "FastAPI endpoint to create a new user with email validation" --language python
```

### Understand Complex Code

```bash
claude-codex explain --file complex_algorithm.py --detail high
```

### Security Review

```bash
claude-codex review --file api.py --aspects security --severity warning
```

### Fix a Bug

```bash
claude-codex debug --file broken.py --error "AttributeError: 'NoneType' object has no attribute 'value'" --expected "Should return default value when None"
```

### Refactor Legacy Code

```bash
claude-codex refactor --file legacy.py --goals readability maintainability
```

### Generate Tests

```bash
claude-codex test --file mymodule.py --language python --framework pytest
```

### Translate to Another Language

```bash
claude-codex translate --file script.py --to javascript
```

## Tips

1. **Be Specific**: The more details you provide, the better the results
2. **Add Context**: Use `--context` to provide information about your project
3. **Iterate**: Generate → Review → Refactor for best results
4. **Use Examples**: Reference existing code in your project as examples

## Next Steps

- Read the full [documentation](CLAUDE_CODEX_README.md)
- Explore [examples](examples/)
- Check out the [API reference](CLAUDE_CODEX_README.md#api-reference)

## Troubleshooting

**Q: "API key must be provided" error**
```bash
export ANTHROPIC_API_KEY="your-key"
```

**Q: Module not found error**
```bash
pip install -e .
```

**Q: Want to use a different model?**
```bash
claude-codex --model claude-opus-4 generate "..."
```

## Get Help

```bash
claude-codex --help
claude-codex generate --help
```

Happy coding! 🚀

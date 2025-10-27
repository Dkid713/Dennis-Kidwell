"""
Super simple example to get started with Claude Codex.

This is the absolute easiest way to use Claude for coding help.
Perfect if you're new to programming!
"""

import os

# First, make sure you have your API key set
# Run this in your terminal before running this script:
# export ANTHROPIC_API_KEY="your-key-here"

# Check if API key is set
if not os.environ.get("ANTHROPIC_API_KEY"):
    print("❌ Please set your ANTHROPIC_API_KEY environment variable!")
    print("Run: export ANTHROPIC_API_KEY='your-key'")
    exit(1)

# Import Claude Codex
from claude_codex import ClaudeCodex
from claude_codex.types import Language

# Create a Claude Codex instance (this connects to Claude)
print("🤖 Connecting to Claude...\n")
codex = ClaudeCodex()


# Example 1: Generate a simple function
print("=" * 60)
print("Example 1: Generate Code")
print("=" * 60)
print("\nAsking Claude to create a function for us...\n")

response = codex.generate_code(
    description="Create a simple function that says hello to a person by name",
    language=Language.PYTHON
)

print(response.content)
print(f"\n(Used {response.tokens_used} tokens)\n")


# Example 2: Explain some code
print("\n" + "=" * 60)
print("Example 2: Explain Code")
print("=" * 60)

my_code = """
def calculate_total(prices):
    return sum(prices) * 1.1
"""

print(f"\nAsking Claude to explain this code:\n{my_code}\n")

response = codex.explain_code(
    code=my_code,
    language=Language.PYTHON,
    detail_level="medium"
)

print(response.content)
print(f"\n(Used {response.tokens_used} tokens)\n")


# Example 3: Fix a bug
print("\n" + "=" * 60)
print("Example 3: Debug Code")
print("=" * 60)

buggy_code = """
def divide_numbers(a, b):
    return a / b

result = divide_numbers(10, 0)
"""

print(f"\nAsking Claude to help debug:\n{buggy_code}\n")

response = codex.debug_code(
    code=buggy_code,
    error_message="ZeroDivisionError: division by zero",
    language=Language.PYTHON
)

print(response.content)
print(f"\n(Used {response.tokens_used} tokens)\n")


# That's it!
print("\n" + "=" * 60)
print("🎉 You did it!")
print("=" * 60)
print("\nThese are the basics of using Claude Codex.")
print("\nNext steps:")
print("  • Try the interactive mode: claude-chat")
print("  • Learn step-by-step: claude-tutor")
print("  • See more examples: python examples/basic_usage.py")
print("\nHappy coding! 🚀\n")

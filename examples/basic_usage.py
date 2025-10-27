"""Basic usage examples for Claude Codex."""

import os
from claude_codex import ClaudeCodex
from claude_codex.types import Language


def example_code_generation():
    """Example: Generate code from natural language."""
    print("=" * 60)
    print("Example 1: Code Generation")
    print("=" * 60)

    codex = ClaudeCodex(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    response = codex.generate_code(
        description="Create a function that checks if a string is a valid email address using regex",
        language=Language.PYTHON,
        context="This will be used in a user registration form validation"
    )

    print(response.content)
    print(f"\nTokens used: {response.tokens_used}")


def example_code_explanation():
    """Example: Explain existing code."""
    print("\n" + "=" * 60)
    print("Example 2: Code Explanation")
    print("=" * 60)

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

    codex = ClaudeCodex(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    response = codex.explain_code(
        code=code,
        language=Language.PYTHON,
        detail_level="medium"
    )

    print(response.content)


def example_code_review():
    """Example: Review code for issues."""
    print("\n" + "=" * 60)
    print("Example 3: Code Review")
    print("=" * 60)

    code = """
def divide(a, b):
    return a / b

def get_user_age(users, user_id):
    for user in users:
        if user['id'] == user_id:
            return user['age']
"""

    codex = ClaudeCodex(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    response = codex.review_code(
        code=code,
        language=Language.PYTHON,
        review_aspects=["security", "bugs", "style"]
    )

    print(response.content)


def example_debugging():
    """Example: Debug problematic code."""
    print("\n" + "=" * 60)
    print("Example 4: Debugging")
    print("=" * 60)

    code = """
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

result = calculate_average([])
"""

    codex = ClaudeCodex(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    response = codex.debug_code(
        code=code,
        error_message="ZeroDivisionError: division by zero",
        expected_behavior="Should handle empty lists gracefully",
        language=Language.PYTHON
    )

    print(response.content)


def example_refactoring():
    """Example: Refactor code."""
    print("\n" + "=" * 60)
    print("Example 5: Code Refactoring")
    print("=" * 60)

    code = """
def process_data(d):
    r = []
    for i in d:
        if i > 0:
            r.append(i * 2)
    return r
"""

    codex = ClaudeCodex(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    response = codex.refactor_code(
        code=code,
        language=Language.PYTHON,
        goals=["readability", "maintainability"]
    )

    print(response.content)


def example_code_translation():
    """Example: Translate code between languages."""
    print("\n" + "=" * 60)
    print("Example 6: Code Translation")
    print("=" * 60)

    js_code = """
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}
"""

    codex = ClaudeCodex(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    response = codex.translate_code(
        code=js_code,
        from_language=Language.JAVASCRIPT,
        to_language=Language.PYTHON
    )

    print(response.content)


def example_test_generation():
    """Example: Generate unit tests."""
    print("\n" + "=" * 60)
    print("Example 7: Test Generation")
    print("=" * 60)

    code = """
def is_palindrome(text):
    text = text.lower().replace(' ', '')
    return text == text[::-1]
"""

    codex = ClaudeCodex(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    response = codex.generate_tests(
        code=code,
        language=Language.PYTHON,
        test_framework="pytest",
        coverage_goals=["edge cases", "normal cases"]
    )

    print(response.content)


def main():
    """Run all examples."""
    # Check if API key is set
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: Please set ANTHROPIC_API_KEY environment variable")
        print("Example: export ANTHROPIC_API_KEY='your-api-key'")
        return

    # Run examples
    example_code_generation()
    example_code_explanation()
    example_code_review()
    example_debugging()
    example_refactoring()
    example_code_translation()
    example_test_generation()


if __name__ == "__main__":
    main()

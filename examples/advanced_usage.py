"""Advanced usage examples for Claude Codex."""

import os
from claude_codex import ClaudeCodex
from claude_codex.types import Language


def example_context_aware_generation():
    """Example: Generate code with extensive context."""
    print("=" * 60)
    print("Advanced Example 1: Context-Aware Code Generation")
    print("=" * 60)

    codex = ClaudeCodex(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    context = """
    We're building a REST API using Flask. We already have:
    - User model with fields: id, username, email, created_at
    - Database connection using SQLAlchemy
    - Authentication middleware that adds 'current_user' to request context
    """

    response = codex.generate_code(
        description="Create an endpoint to update user profile (email and username)",
        language=Language.PYTHON,
        context=context,
        constraints=[
            "Must validate email format",
            "Must check if new username is already taken",
            "Must require authentication",
            "Return appropriate HTTP status codes"
        ]
    )

    print(response.content)


def example_custom_style_guide():
    """Example: Generate code following specific style guide."""
    print("\n" + "=" * 60)
    print("Advanced Example 2: Custom Style Guide")
    print("=" * 60)

    codex = ClaudeCodex(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    style_guide = """
    - Use TypeScript strict mode
    - Prefer functional components over class components
    - Use arrow functions consistently
    - Add JSDoc comments for all functions
    - Use async/await instead of .then()
    """

    response = codex.generate_code(
        description="Create a React component that fetches and displays a list of products from an API",
        language=Language.TYPESCRIPT,
        style_guide=style_guide
    )

    print(response.content)


def example_detailed_code_explanation():
    """Example: Deep dive code explanation."""
    print("\n" + "=" * 60)
    print("Advanced Example 3: Detailed Code Explanation")
    print("=" * 60)

    complex_code = """
class LRUCache:
    def __init__(self, capacity: int):
        self.cache = {}
        self.capacity = capacity
        self.order = []

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.order.remove(key)
        self.order.append(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest = self.order.pop(0)
            del self.cache[oldest]
        self.cache[key] = value
        self.order.append(key)
"""

    codex = ClaudeCodex(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    response = codex.explain_code(
        code=complex_code,
        language=Language.PYTHON,
        detail_level="high",
        focus_areas=["algorithm", "time complexity", "space complexity", "design patterns"]
    )

    print(response.content)


def example_security_focused_review():
    """Example: Security-focused code review."""
    print("\n" + "=" * 60)
    print("Advanced Example 4: Security-Focused Review")
    print("=" * 60)

    potentially_vulnerable_code = """
import sqlite3
from flask import Flask, request

app = Flask(__name__)

@app.route('/search')
def search_users():
    query = request.args.get('q')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE name LIKE '%{query}%'")
    results = cursor.fetchall()
    conn.close()
    return {'users': results}

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Check credentials...
    return {'token': generate_token(username)}
"""

    codex = ClaudeCodex(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    response = codex.review_code(
        code=potentially_vulnerable_code,
        language=Language.PYTHON,
        review_aspects=["security", "sql injection", "authentication", "data exposure"],
        severity_threshold="warning"
    )

    print(response.content)


def example_performance_refactoring():
    """Example: Refactor for performance."""
    print("\n" + "=" * 60)
    print("Advanced Example 5: Performance-Focused Refactoring")
    print("=" * 60)

    slow_code = """
def find_duplicates(list1, list2):
    duplicates = []
    for item1 in list1:
        for item2 in list2:
            if item1 == item2 and item1 not in duplicates:
                duplicates.append(item1)
    return duplicates

def process_large_dataset(data):
    results = []
    for i in range(len(data)):
        item = data[i]
        if is_valid(item):
            results.append(transform(item))
    return results
"""

    codex = ClaudeCodex(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    response = codex.refactor_code(
        code=slow_code,
        language=Language.PYTHON,
        goals=["performance", "time complexity"],
        constraints=[
            "Maintain the same functionality",
            "Optimize for large datasets (1M+ items)",
            "Use appropriate data structures"
        ]
    )

    print(response.content)


def example_multi_file_documentation():
    """Example: Generate comprehensive documentation."""
    print("\n" + "=" * 60)
    print("Advanced Example 6: Comprehensive Documentation")
    print("=" * 60)

    module_code = """
class DataProcessor:
    def __init__(self, config):
        self.config = config
        self.pipeline = self._build_pipeline()

    def _build_pipeline(self):
        return [
            self._validate,
            self._transform,
            self._enrich,
            self._aggregate
        ]

    def process(self, data):
        result = data
        for step in self.pipeline:
            result = step(result)
        return result

    def _validate(self, data):
        # Validation logic
        pass

    def _transform(self, data):
        # Transformation logic
        pass

    def _enrich(self, data):
        # Enrichment logic
        pass

    def _aggregate(self, data):
        # Aggregation logic
        pass
"""

    codex = ClaudeCodex(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    response = codex.generate_documentation(
        code=module_code,
        language=Language.PYTHON,
        doc_format="markdown"
    )

    print(response.content)


def example_batch_processing():
    """Example: Process multiple code files."""
    print("\n" + "=" * 60)
    print("Advanced Example 7: Batch Code Analysis")
    print("=" * 60)

    codex = ClaudeCodex(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    code_snippets = {
        "auth.py": "def authenticate(token): return verify_jwt(token)",
        "utils.py": "def format_date(d): return d.strftime('%Y-%m-%d')",
        "api.py": "def get_users(): return db.query('SELECT * FROM users')"
    }

    print("Analyzing multiple files...\n")

    for filename, code in code_snippets.items():
        print(f"\n--- {filename} ---")
        response = codex.review_code(
            code=code,
            language=Language.PYTHON,
            review_aspects=["security", "best practices"]
        )
        print(response.content[:200] + "..." if len(response.content) > 200 else response.content)


def main():
    """Run all advanced examples."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: Please set ANTHROPIC_API_KEY environment variable")
        return

    example_context_aware_generation()
    example_custom_style_guide()
    example_detailed_code_explanation()
    example_security_focused_review()
    example_performance_refactoring()
    example_multi_file_documentation()
    example_batch_processing()


if __name__ == "__main__":
    main()

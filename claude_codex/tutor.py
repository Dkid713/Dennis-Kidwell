#!/usr/bin/env python3
"""
Beginner-friendly coding tutor mode.

Teaches programming step-by-step with Claude's help.
"""

import os
import sys
from typing import Optional
from .client import ClaudeCodex
from .types import Language


class CodingTutor:
    """Step-by-step coding tutor for beginners."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the tutor."""
        try:
            self.codex = ClaudeCodex(api_key=api_key, temperature=0.7)
        except ValueError:
            print("\n❌ Error: You need to set your ANTHROPIC_API_KEY")
            print("Get your API key from: https://console.anthropic.com/settings/keys")
            print("\nThen run:")
            print("  export ANTHROPIC_API_KEY='your-key-here'")
            sys.exit(1)

    def welcome(self):
        """Welcome message."""
        print("\n" + "=" * 70)
        print("🎓 CLAUDE CODING TUTOR")
        print("=" * 70)
        print("\nHi! I'm Claude, your personal coding tutor.")
        print("I'll teach you programming step-by-step at your own pace.")
        print("\nNo question is too basic - I'm here to help you learn!")
        print("=" * 70 + "\n")

    def choose_topic(self) -> Optional[str]:
        """Let user choose what to learn."""
        print("\n📚 What would you like to learn about?")
        print()
        print("Beginner Topics:")
        print("  1. Python Basics (variables, functions, loops)")
        print("  2. Working with Lists and Dictionaries")
        print("  3. File Reading and Writing")
        print("  4. Error Handling (try/except)")
        print()
        print("Intermediate Topics:")
        print("  5. Object-Oriented Programming (Classes)")
        print("  6. Working with APIs")
        print("  7. Web Scraping")
        print()
        print("Project-Based:")
        print("  8. Build a Calculator")
        print("  9. Build a To-Do List App")
        print("  10. Build a Simple Game")
        print()
        print("  0. Ask a custom question")
        print()

        choice = input("Choose a topic (0-10) or 'quit' to exit: ").strip()

        if choice.lower() in ['quit', 'exit', 'q']:
            return None

        topics = {
            "1": "Python basics: teach me about variables, functions, and loops with simple examples",
            "2": "Python lists and dictionaries: teach me with practical examples",
            "3": "How to read and write files in Python with examples",
            "4": "Error handling in Python: try/except blocks with examples",
            "5": "Object-oriented programming in Python: classes and objects with examples",
            "6": "How to work with APIs in Python: making HTTP requests with examples",
            "7": "Web scraping with Python: BeautifulSoup tutorial with examples",
            "8": "Help me build a calculator program in Python step-by-step",
            "9": "Help me build a to-do list application in Python step-by-step",
            "10": "Help me build a simple text-based game in Python step-by-step",
        }

        if choice == "0":
            custom = input("\n💬 What do you want to learn? ").strip()
            return custom if custom else None

        return topics.get(choice)

    def teach(self, topic: str):
        """Teach a topic."""
        print(f"\n🎯 Learning: {topic}")
        print("\n💭 Let me prepare a lesson for you...\n")
        print("-" * 70)

        try:
            # Generate a comprehensive lesson
            response = self.codex.generate_code(
                description=f"""Create a beginner-friendly tutorial for: {topic}

The tutorial should:
1. Start with a simple explanation
2. Include step-by-step code examples
3. Explain each part of the code
4. Include practice exercises
5. Be encouraging and easy to understand

Make it conversational and friendly for someone just learning to code.""",
                language=Language.PYTHON,
                context="This is for a complete beginner learning to code"
            )

            print(response.content)
            print("\n" + "-" * 70)

            # Offer practice
            print("\n📝 Would you like to:")
            print("  1. Try a practice exercise")
            print("  2. Ask a follow-up question")
            print("  3. Learn something else")
            print("  4. Go back to menu")

            choice = input("\nYour choice (1-4): ").strip()

            if choice == "1":
                self.practice_mode(topic)
            elif choice == "2":
                self.qa_mode(topic)
            elif choice == "3":
                return
            else:
                return

        except Exception as e:
            print(f"\n❌ Error: {e}")

    def practice_mode(self, topic: str):
        """Interactive practice."""
        print("\n🏋️ Practice Mode")
        print("\nWrite your code below (type END on a new line when done):")
        print()

        lines = []
        try:
            while True:
                line = input(">>> ")
                if line.strip().upper() == 'END':
                    break
                lines.append(line)
        except KeyboardInterrupt:
            print("\n")
            return

        code = '\n'.join(lines)

        if not code.strip():
            print("No code entered!")
            return

        # Get feedback
        print("\n💭 Reviewing your code...\n")

        try:
            response = self.codex.review_code(
                code=code,
                language=Language.PYTHON,
                review_aspects=["correctness", "style", "beginner-friendly suggestions"]
            )

            print(response.content)

            # Offer to fix
            fix = input("\n\nWould you like me to show an improved version? (y/n): ")
            if fix.lower() == 'y':
                improved = self.codex.refactor_code(
                    code=code,
                    language=Language.PYTHON,
                    goals=["readability", "best practices", "beginner-friendly"]
                )
                print("\n✨ Improved version:\n")
                print(improved.content)

        except Exception as e:
            print(f"\n❌ Error: {e}")

    def qa_mode(self, topic: str):
        """Q&A mode."""
        print("\n❓ Ask Your Question")
        question = input("\n💬 You: ").strip()

        if not question:
            return

        print("\n💭 Thinking...\n")

        try:
            response = self.codex.generate_code(
                description=f"Answer this beginner question about {topic}: {question}. Explain in simple terms with examples.",
                language=Language.PYTHON,
                context="Answering a beginner's question"
            )

            print(response.content)

        except Exception as e:
            print(f"\n❌ Error: {e}")

    def run(self):
        """Run the tutor."""
        self.welcome()

        while True:
            topic = self.choose_topic()

            if topic is None:
                print("\n👋 Keep learning! You're doing great!")
                break

            self.teach(topic)

        print("\n🎉 Happy coding!\n")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Claude Coding Tutor - Learn to code step-by-step'
    )

    parser.add_argument(
        '--api-key',
        help='Anthropic API key (or set ANTHROPIC_API_KEY env var)'
    )

    args = parser.parse_args()

    tutor = CodingTutor(api_key=args.api_key)
    tutor.run()


if __name__ == '__main__':
    main()

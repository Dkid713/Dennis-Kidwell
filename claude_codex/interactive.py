#!/usr/bin/env python3
"""
Interactive Replit-style coding assistant powered by Claude.

This provides a simple, beginner-friendly interface for getting coding help.
"""

import os
import sys
from typing import Optional
from .client import ClaudeCodex
from .types import Language


class InteractiveCodingAssistant:
    """Interactive coding assistant - like having Claude as your pair programmer."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the assistant."""
        try:
            self.codex = ClaudeCodex(api_key=api_key, temperature=0.5)
            self.conversation_history = []
            self.current_language = Language.PYTHON
        except ValueError as e:
            print("\n❌ Error: You need to set your ANTHROPIC_API_KEY")
            print("Get your API key from: https://console.anthropic.com/settings/keys")
            print("\nThen run:")
            print("  export ANTHROPIC_API_KEY='your-key-here'")
            sys.exit(1)

    def welcome(self):
        """Display welcome message."""
        print("\n" + "=" * 70)
        print("🤖 CLAUDE CODING ASSISTANT - Interactive Mode")
        print("=" * 70)
        print("\nHey! I'm Claude, your AI coding buddy. I'm here to help you code!")
        print("\nWhat I can help with:")
        print("  • Write code for you")
        print("  • Explain code you don't understand")
        print("  • Fix bugs and errors")
        print("  • Review and improve your code")
        print("  • Teach you programming concepts")
        print("  • Answer coding questions")
        print("\nCommands:")
        print("  /help     - Show this help")
        print("  /new      - Start fresh (clear history)")
        print("  /lang     - Change programming language")
        print("  /quit     - Exit")
        print("\nJust type what you need help with, or paste your code!")
        print("=" * 70 + "\n")

    def set_language(self):
        """Let user choose programming language."""
        print("\n📝 Available languages:")
        languages = [
            ("1", "Python", Language.PYTHON),
            ("2", "JavaScript", Language.JAVASCRIPT),
            ("3", "TypeScript", Language.TYPESCRIPT),
            ("4", "Java", Language.JAVA),
            ("5", "C++", Language.CPP),
            ("6", "Go", Language.GO),
            ("7", "Rust", Language.RUST),
            ("8", "Ruby", Language.RUBY),
            ("9", "Other", Language.AUTO),
        ]

        for num, name, _ in languages:
            print(f"  {num}. {name}")

        choice = input("\nChoose (1-9) or press Enter for Python: ").strip()

        if not choice:
            choice = "1"

        for num, name, lang in languages:
            if choice == num:
                self.current_language = lang
                print(f"✓ Switched to {name}")
                return

        print("Invalid choice, staying with current language")

    def detect_intent(self, user_input: str) -> str:
        """Figure out what the user wants to do."""
        user_lower = user_input.lower().strip()

        # Check if it's a question
        if any(q in user_lower for q in ["what is", "how do", "can you explain", "why", "?"]):
            return "explain"

        # Check if it's code to review/debug
        if any(word in user_lower for word in ["def ", "function", "class ", "import ", "{", "}", "error", "bug", "doesn't work", "not working"]):
            if any(word in user_lower for word in ["error", "bug", "wrong", "doesn't work", "not working", "broken"]):
                return "debug"
            return "review"

        # Check if they want code generation
        if any(word in user_lower for word in ["create", "write", "make", "build", "generate", "code for"]):
            return "generate"

        # Default to generate
        return "generate"

    def handle_request(self, user_input: str):
        """Process user request and get Claude's help."""
        intent = self.detect_intent(user_input)

        try:
            if intent == "generate":
                print("\n💭 Generating code for you...\n")
                response = self.codex.generate_code(
                    description=user_input,
                    language=self.current_language
                )

            elif intent == "explain":
                print("\n💭 Let me explain...\n")
                # Check if they included code
                if any(word in user_input for word in ["def ", "function", "class ", "import "]):
                    response = self.codex.explain_code(
                        code=user_input,
                        language=self.current_language,
                        detail_level="high"
                    )
                else:
                    # It's a general question, use generate to answer
                    response = self.codex.generate_code(
                        description=f"Explain: {user_input}",
                        language=self.current_language
                    )

            elif intent == "debug":
                print("\n🔍 Debugging your code...\n")
                response = self.codex.debug_code(
                    code=user_input,
                    language=self.current_language
                )

            elif intent == "review":
                print("\n👀 Reviewing your code...\n")
                response = self.codex.review_code(
                    code=user_input,
                    language=self.current_language,
                    review_aspects=["bugs", "style", "best practices"]
                )

            # Display response
            print(response.content)
            print(f"\n💡 Tokens used: {response.tokens_used}")

            # Save to history
            self.conversation_history.append({
                "user": user_input,
                "assistant": response.content
            })

        except Exception as e:
            print(f"\n❌ Oops, something went wrong: {e}")
            print("Try rephrasing your question or check your API key.")

    def multiline_input(self) -> Optional[str]:
        """Allow multi-line input for pasting code."""
        print("\n💬 What do you need help with?")
        print("   (Type your question, paste code, or use /command)")
        print("   (Press Ctrl+D or type END on a new line when done)")
        print()

        lines = []
        try:
            while True:
                line = input("   ")

                # Check for commands
                if line.strip().lower() in ['/quit', '/exit', '/q']:
                    return None

                if line.strip().lower() == '/help':
                    return '/help'

                if line.strip().lower() == '/new':
                    return '/new'

                if line.strip().lower() == '/lang':
                    return '/lang'

                # Check for END marker
                if line.strip().upper() == 'END':
                    break

                lines.append(line)

        except EOFError:
            # Ctrl+D pressed
            pass
        except KeyboardInterrupt:
            print("\n\n👋 Use /quit to exit properly!")
            return ""

        result = '\n'.join(lines).strip()
        return result if result else ""

    def simple_input(self) -> Optional[str]:
        """Simple single-line input mode."""
        try:
            user_input = input("\n💬 You: ").strip()
            return user_input
        except KeyboardInterrupt:
            print("\n\n👋 Use /quit to exit!")
            return ""
        except EOFError:
            return None

    def run(self, simple_mode: bool = False):
        """Run the interactive assistant."""
        self.welcome()

        while True:
            # Get user input
            if simple_mode:
                user_input = self.simple_input()
            else:
                user_input = self.multiline_input()

            if user_input is None:
                print("\n👋 Goodbye! Happy coding!")
                break

            if not user_input:
                continue

            # Handle commands
            if user_input.lower() in ['/quit', '/exit', '/q']:
                print("\n👋 Goodbye! Happy coding!")
                break

            if user_input.lower() == '/help':
                self.welcome()
                continue

            if user_input.lower() == '/new':
                self.conversation_history = []
                print("\n✓ Starting fresh! History cleared.")
                continue

            if user_input.lower() == '/lang':
                self.set_language()
                continue

            # Process the request
            self.handle_request(user_input)


def main():
    """Main entry point for interactive mode."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Interactive Claude Coding Assistant',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start interactive mode
  claude-codex-chat

  # Use simple single-line mode
  claude-codex-chat --simple

  # Set API key
  export ANTHROPIC_API_KEY='your-key'
  claude-codex-chat
        """
    )

    parser.add_argument(
        '--api-key',
        help='Anthropic API key (or set ANTHROPIC_API_KEY env var)'
    )

    parser.add_argument(
        '--simple',
        action='store_true',
        help='Use simple single-line input mode'
    )

    args = parser.parse_args()

    # Create and run assistant
    assistant = InteractiveCodingAssistant(api_key=args.api_key)
    assistant.run(simple_mode=args.simple)


if __name__ == '__main__':
    main()

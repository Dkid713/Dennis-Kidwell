#!/usr/bin/env python3
"""Command-line interface for Claude Codex."""

import sys
import argparse
from pathlib import Path
from typing import Optional

from .client import ClaudeCodex
from .types import Language, CodexMode


def read_file_or_stdin(file_path: Optional[str]) -> str:
    """Read from file or stdin if file_path is None or '-'."""
    if file_path is None or file_path == '-':
        return sys.stdin.read()
    return Path(file_path).read_text()


def detect_language_from_file(file_path: str) -> Language:
    """Detect programming language from file extension."""
    ext_map = {
        '.py': Language.PYTHON,
        '.js': Language.JAVASCRIPT,
        '.ts': Language.TYPESCRIPT,
        '.java': Language.JAVA,
        '.cpp': Language.CPP,
        '.cc': Language.CPP,
        '.cxx': Language.CPP,
        '.cs': Language.CSHARP,
        '.go': Language.GO,
        '.rs': Language.RUST,
        '.rb': Language.RUBY,
        '.php': Language.PHP,
        '.swift': Language.SWIFT,
        '.kt': Language.KOTLIN,
        '.sql': Language.SQL,
        '.html': Language.HTML,
        '.css': Language.CSS,
        '.sh': Language.SHELL,
        '.bash': Language.SHELL,
    }
    ext = Path(file_path).suffix.lower()
    return ext_map.get(ext, Language.AUTO)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Claude Codex - AI-powered code intelligence using Claude by Anthropic',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate code
  claude-codex generate "fibonacci function" --language python

  # Explain code
  claude-codex explain --file script.py

  # Review code
  claude-codex review --file app.js --aspects security performance

  # Debug code with error
  claude-codex debug --file buggy.py --error "ValueError: invalid literal"

  # Refactor code
  claude-codex refactor --file legacy.py --goals readability performance

  # Generate tests
  claude-codex test --file mycode.py --framework pytest

  # Translate code
  claude-codex translate --file script.js --to python
        """
    )

    parser.add_argument(
        '--api-key',
        help='Anthropic API key (or set ANTHROPIC_API_KEY env var)',
    )
    parser.add_argument(
        '--model',
        default='claude-sonnet-4-20250514',
        help='Claude model to use (default: claude-sonnet-4-20250514)',
    )
    parser.add_argument(
        '--temperature',
        type=float,
        default=0.3,
        help='Sampling temperature 0.0-1.0 (default: 0.3)',
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Generate command
    gen_parser = subparsers.add_parser('generate', aliases=['gen'], help='Generate code from description')
    gen_parser.add_argument('description', help='Description of code to generate')
    gen_parser.add_argument('-l', '--language', required=True, choices=[l.value for l in Language if l != Language.AUTO])
    gen_parser.add_argument('-c', '--context', help='Additional context')
    gen_parser.add_argument('--style', help='Style guide to follow')

    # Explain command
    exp_parser = subparsers.add_parser('explain', help='Explain what code does')
    exp_parser.add_argument('-f', '--file', help='File to explain (use - for stdin)')
    exp_parser.add_argument('-l', '--language', choices=[l.value for l in Language])
    exp_parser.add_argument('-d', '--detail', choices=['low', 'medium', 'high'], default='medium')

    # Review command
    rev_parser = subparsers.add_parser('review', help='Review code for issues')
    rev_parser.add_argument('-f', '--file', help='File to review (use - for stdin)')
    rev_parser.add_argument('-l', '--language', choices=[l.value for l in Language])
    rev_parser.add_argument('-a', '--aspects', nargs='+', help='Aspects to review (security, performance, style, etc.)')
    rev_parser.add_argument('-s', '--severity', choices=['all', 'warning', 'error'], default='all')

    # Debug command
    dbg_parser = subparsers.add_parser('debug', help='Debug code and find issues')
    dbg_parser.add_argument('-f', '--file', help='File to debug (use - for stdin)')
    dbg_parser.add_argument('-l', '--language', choices=[l.value for l in Language])
    dbg_parser.add_argument('-e', '--error', help='Error message')
    dbg_parser.add_argument('-x', '--expected', help='Expected behavior')
    dbg_parser.add_argument('-c', '--context', help='Additional context')

    # Refactor command
    ref_parser = subparsers.add_parser('refactor', help='Refactor code to improve quality')
    ref_parser.add_argument('-f', '--file', help='File to refactor (use - for stdin)')
    ref_parser.add_argument('-l', '--language', choices=[l.value for l in Language])
    ref_parser.add_argument('-g', '--goals', nargs='+', help='Refactoring goals (readability, performance, etc.)')

    # Complete command
    cmp_parser = subparsers.add_parser('complete', help='Complete partial code')
    cmp_parser.add_argument('-f', '--file', help='File with partial code (use - for stdin)')
    cmp_parser.add_argument('-l', '--language', required=True, choices=[l.value for l in Language if l != Language.AUTO])
    cmp_parser.add_argument('-c', '--context', help='Additional context')

    # Document command
    doc_parser = subparsers.add_parser('document', aliases=['doc'], help='Generate documentation')
    doc_parser.add_argument('-f', '--file', help='File to document (use - for stdin)')
    doc_parser.add_argument('-l', '--language', choices=[l.value for l in Language])
    doc_parser.add_argument('--format', default='markdown', help='Documentation format')

    # Translate command
    trs_parser = subparsers.add_parser('translate', help='Translate code between languages')
    trs_parser.add_argument('-f', '--file', help='File to translate (use - for stdin)')
    trs_parser.add_argument('--from', dest='from_lang', choices=[l.value for l in Language if l != Language.AUTO])
    trs_parser.add_argument('--to', required=True, choices=[l.value for l in Language if l != Language.AUTO])

    # Test command
    tst_parser = subparsers.add_parser('test', help='Generate unit tests')
    tst_parser.add_argument('-f', '--file', help='File to test (use - for stdin)')
    tst_parser.add_argument('-l', '--language', required=True, choices=[l.value for l in Language if l != Language.AUTO])
    tst_parser.add_argument('--framework', help='Testing framework (pytest, jest, junit, etc.)')
    tst_parser.add_argument('--coverage', nargs='+', help='Coverage goals')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Initialize client
    try:
        codex = ClaudeCodex(
            api_key=args.api_key,
            model=args.model,
            temperature=args.temperature,
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Execute command
    try:
        response = None

        if args.command in ['generate', 'gen']:
            response = codex.generate_code(
                description=args.description,
                language=Language(args.language),
                context=args.context,
                style_guide=args.style,
            )

        elif args.command == 'explain':
            code = read_file_or_stdin(args.file)
            lang = Language(args.language) if args.language else detect_language_from_file(args.file) if args.file else Language.AUTO
            response = codex.explain_code(
                code=code,
                language=lang,
                detail_level=args.detail,
            )

        elif args.command == 'review':
            code = read_file_or_stdin(args.file)
            lang = Language(args.language) if args.language else detect_language_from_file(args.file) if args.file else Language.AUTO
            response = codex.review_code(
                code=code,
                language=lang,
                review_aspects=args.aspects,
                severity_threshold=args.severity,
            )

        elif args.command == 'debug':
            code = read_file_or_stdin(args.file)
            lang = Language(args.language) if args.language else detect_language_from_file(args.file) if args.file else Language.AUTO
            response = codex.debug_code(
                code=code,
                error_message=args.error,
                expected_behavior=args.expected,
                language=lang,
                context=args.context,
            )

        elif args.command == 'refactor':
            code = read_file_or_stdin(args.file)
            lang = Language(args.language) if args.language else detect_language_from_file(args.file) if args.file else Language.AUTO
            response = codex.refactor_code(
                code=code,
                language=lang,
                goals=args.goals,
            )

        elif args.command == 'complete':
            code = read_file_or_stdin(args.file)
            response = codex.complete_code(
                code_prefix=code,
                language=Language(args.language),
                context=args.context,
            )

        elif args.command in ['document', 'doc']:
            code = read_file_or_stdin(args.file)
            lang = Language(args.language) if args.language else detect_language_from_file(args.file) if args.file else Language.AUTO
            response = codex.generate_documentation(
                code=code,
                language=lang,
                doc_format=args.format,
            )

        elif args.command == 'translate':
            code = read_file_or_stdin(args.file)
            from_lang = Language(args.from_lang) if args.from_lang else detect_language_from_file(args.file) if args.file else Language.AUTO
            response = codex.translate_code(
                code=code,
                from_language=from_lang,
                to_language=Language(args.to),
            )

        elif args.command == 'test':
            code = read_file_or_stdin(args.file)
            response = codex.generate_tests(
                code=code,
                language=Language(args.language),
                test_framework=args.framework,
                coverage_goals=args.coverage,
            )

        # Output response
        if response:
            print(response.content)
            if response.tokens_used:
                print(f"\n[Tokens used: {response.tokens_used}]", file=sys.stderr)
            return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())

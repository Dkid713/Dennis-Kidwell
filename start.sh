#!/bin/bash
#
# Easy setup script for Claude Codex
# Run with: bash start.sh
#

echo "================================================"
echo "🤖 CLAUDE CODEX - Easy Setup"
echo "================================================"
echo ""

# Check if API key is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  API key not found!"
    echo ""
    echo "You need to set your Anthropic API key."
    echo ""
    echo "1. Get your key from: https://console.anthropic.com/settings/keys"
    echo "2. Then run:"
    echo "   export ANTHROPIC_API_KEY='your-key-here'"
    echo ""
    echo "Or add it permanently to your ~/.bashrc:"
    echo "   echo 'export ANTHROPIC_API_KEY=\"your-key\"' >> ~/.bashrc"
    echo "   source ~/.bashrc"
    echo ""
    exit 1
fi

echo "✓ API key found!"
echo ""

# Check if already installed
if command -v claude-chat &> /dev/null; then
    echo "✓ Claude Codex is already installed!"
    echo ""
else
    echo "📦 Installing Claude Codex..."
    pip install -e . -q

    if [ $? -eq 0 ]; then
        echo "✓ Installation complete!"
        echo ""
    else
        echo "❌ Installation failed. Try: pip install -e ."
        exit 1
    fi
fi

echo "================================================"
echo "🎉 You're all set!"
echo "================================================"
echo ""
echo "Choose how you want to start:"
echo ""
echo "  1) 🎓 TUTOR MODE - Learn to code step-by-step"
echo "  2) 💬 CHAT MODE - Interactive coding assistant"
echo "  3) ⚡ See quick command examples"
echo "  4) 📖 Read the guide"
echo "  5) Exit"
echo ""

read -p "Your choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "Starting Claude Tutor..."
        echo ""
        claude-tutor
        ;;
    2)
        echo ""
        echo "Starting Claude Chat..."
        echo ""
        claude-chat
        ;;
    3)
        echo ""
        echo "Quick Commands:"
        echo ""
        echo "Generate code:"
        echo '  claude-codex generate "function to add two numbers" --language python'
        echo ""
        echo "Explain code:"
        echo '  echo "def hello(): return \"hi\"" | claude-codex explain -'
        echo ""
        echo "Chat mode:"
        echo "  claude-chat"
        echo ""
        echo "Tutor mode:"
        echo "  claude-tutor"
        echo ""
        echo "Get help:"
        echo "  claude-codex --help"
        echo ""
        ;;
    4)
        echo ""
        echo "Opening guide..."
        cat EASY_START.md
        ;;
    5)
        echo ""
        echo "👋 Happy coding!"
        exit 0
        ;;
    *)
        echo ""
        echo "Invalid choice. Run './start.sh' again."
        exit 1
        ;;
esac

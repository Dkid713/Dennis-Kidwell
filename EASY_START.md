# 🚀 Super Easy Start Guide

**No experience needed! Let's get you coding with Claude's help.**

---

## Step 1: Get Your API Key (2 minutes)

1. Go to: https://console.anthropic.com/settings/keys
2. Click "Create Key"
3. Copy your key (starts with `sk-ant-api03-...`)
4. **Keep it secret!** Don't share it.

---

## Step 2: Install (1 minute)

Open your terminal and run these commands **one at a time**:

```bash
cd ~
git clone https://github.com/Dkid713/Dennis-Kidwell.git
cd Dennis-Kidwell
git checkout claude/create-claude-codex-011CUYVuUJbjPrfBZjxV2bwW
pip install -e .
```

---

## Step 3: Set Your API Key (30 seconds)

Replace `YOUR_KEY_HERE` with your actual key:

```bash
export ANTHROPIC_API_KEY="YOUR_KEY_HERE"
```

**💡 Tip**: Add this to your `~/.bashrc` so you don't have to type it every time:
```bash
echo 'export ANTHROPIC_API_KEY="YOUR_KEY_HERE"' >> ~/.bashrc
```

---

## Step 4: Start Coding! (Now!)

You have **3 easy ways** to use Claude:

### 🎓 Option 1: TUTOR MODE (Best for Beginners!)

Learn to code step-by-step:

```bash
claude-tutor
```

This will:
- Teach you programming from scratch
- Give you practice exercises
- Answer all your questions
- Be patient and encouraging!

---

### 💬 Option 2: CHAT MODE (Like Replit!)

Interactive coding assistant:

```bash
claude-chat
```

Just type what you want:
- "create a function that adds two numbers"
- "explain this code: def hello(): print('hi')"
- "why is my code broken?"
- Paste your code and ask for help!

---

### ⚡ Option 3: QUICK COMMANDS

Fast one-line commands:

```bash
# Generate code
claude-codex generate "function to check if number is even" --language python

# Explain code
echo "def double(x): return x * 2" | claude-codex explain -

# Fix bugs
claude-codex debug --file mycode.py
```

---

## Example Session

```bash
$ claude-chat

🤖 CLAUDE CODING ASSISTANT - Interactive Mode
===============================================

Hey! I'm Claude, your AI coding buddy. I'm here to help you code!

💬 What do you need help with?

   create a function that reverses a string

💭 Generating code for you...

```python
def reverse_string(text: str) -> str:
    """
    Reverse a string.

    Args:
        text: The string to reverse

    Returns:
        The reversed string
    """
    return text[::-1]

# Example usage:
print(reverse_string("hello"))  # Output: "olleh"
```

💡 Tokens used: 156

💬 What do you need help with?
```

---

## Common Questions

**Q: "I'm getting an API key error"**

Make sure you:
1. Set the environment variable: `export ANTHROPIC_API_KEY="your-key"`
2. Used your ACTUAL key (not the example text)
3. Didn't add extra quotes or spaces

**Q: "Command not found"**

Run: `pip install -e .` in the Dennis-Kidwell directory

**Q: "I'm completely new to programming"**

Perfect! Start with:
```bash
claude-tutor
```
Then choose option 1 (Python Basics)

**Q: "Can I use this for JavaScript/Java/etc?"**

Yes! Use `/lang` in chat mode, or add `--language javascript` to commands

**Q: "How much does this cost?"**

You pay for Claude API usage. Very cheap for learning:
- ~$0.003 per code generation
- ~$0.015 per detailed explanation
- https://www.anthropic.com/pricing

---

## Quick Reference Card

```
TUTOR MODE (learning):     claude-tutor
CHAT MODE (interactive):   claude-chat
QUICK GENERATE:            claude-codex generate "..." --language python
EXPLAIN CODE:              claude-codex explain --file code.py
FIX BUGS:                  claude-codex debug --file broken.py
IMPROVE CODE:              claude-codex refactor --file messy.py
GET HELP:                  claude-codex --help
```

---

## What Next?

1. **Just start!** Run `claude-chat` and ask it anything
2. **Learn systematically** with `claude-tutor`
3. **Build something** - Ask Claude to help you build a project!
4. **Read docs** - Check CLAUDE_CODEX_README.md for advanced features

---

## You Got This! 🎉

Remember:
- **No question is too basic** - Claude is here to help
- **Mistakes are learning** - That's how you get better
- **Experiment freely** - Try things out!
- **Ask for explanations** - "Why does this work?"

**Start now:**
```bash
claude-chat
```

Type: "teach me to code"

---

**Need help? Have questions?**
- Open an issue: https://github.com/Dkid713/Dennis-Kidwell/issues
- The community is here to help!

Happy coding! 🚀

# Code Generator Bot

A simple CLI tool that generates beginner-friendly Python code templates for small programs.

Features
- Generates code for: Factorial, Prime Checker, Palindrome Checker, Fibonacci, Even/Odd
- Dictionary-based registry (easy to extend)
- No external libraries required (pure Python)
- Option to save generated code to a .py file
- Continuous loop until you type `exit`

Usage

Run the bot:

```bash
python3 main.py
```

Follow prompts to select a program and provide inputs. After code is displayed, choose whether to save it to a file.

Extending

Add new entries to the `PROGRAMS` dictionary in `main.py`. Each program should define `display`, `description`, `inputs`, and `variants` (templates).

License

MIT-style: use freely for learning and experimentation.
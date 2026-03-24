#!/usr/bin/env python3
"""
Code Generator Bot

Single-file CLI that generates beginner-friendly Python code templates
for small programs (factorial, prime, palindrome, fibonacci, even/odd).

No external libraries. Loop continues until user types "exit".
"""

import sys


# -----------------------------
# Program registry (dictionary)
# -----------------------------
# Each entry defines: display, description, inputs (list), template(s)
PROGRAMS = {
    "factorial": {
        "display": "Factorial",
        "description": "Compute factorial of a non-negative integer",
        "variants": {
            "iterative": {
                "description": "Iterative implementation",
                "template": (
                    "def factorial(n):\n"
                    "    \"\"\"Return factorial of n (iterative).\"\"\"\n"
                    "    if n < 0:\n"
                    "        raise ValueError('Negative input not allowed')\n"
                    "    result = 1\n"
                    "    for i in range(2, n + 1):\n"
                    "        result *= i\n"
                    "    return result\n\n"
                    "# Example usage:\n"
                    "print('factorial({user_n}) =', factorial({user_n}))\n"
                )
            },
            "recursive": {
                "description": "Recursive implementation",
                "template": (
                    "def factorial(n):\n"
                    "    \"\"\"Return factorial of n (recursive).\"\"\"\n"
                    "    if n < 0:\n"
                    "        raise ValueError('Negative input not allowed')\n"
                    "    if n <= 1:\n"
                    "        return 1\n"
                    "    return n * factorial(n - 1)\n\n"
                    "# Example usage:\n"
                    "print('factorial({user_n}) =', factorial({user_n}))\n"
                )
            }
        },
        "inputs": [{"name": "user_n", "type": "int", "prompt": "Enter a non-negative integer"}],
    },

    "prime": {
        "display": "Prime Checker",
        "description": "Check whether a number is prime",
        "variants": {
            "basic": {
                "description": "Simple loop-based prime check",
                "template": (
                    "def is_prime(n):\n"
                    "    \"\"\"Return True if n is prime (n >= 2).\"\"\"\n"
                    "    if n <= 1:\n"
                    "        return False\n"
                    "    if n <= 3:\n"
                    "        return True\n"
                    "    if n % 2 == 0:\n"
                    "        return False\n"
                    "    i = 3\n"
                    "    while i * i <= n:\n"
                    "        if n % i == 0:\n"
                    "            return False\n"
                    "        i += 2\n"
                    "    return True\n\n"
                    "# Example usage:\n"
                    "print(f'is_prime({user_n}) =', is_prime({user_n}))\n"
                )
            }
        },
        "inputs": [{"name": "user_n", "type": "int", "prompt": "Enter an integer (>=0)"}],
    },

    "palindrome": {
        "display": "Palindrome Checker",
        "description": "Check whether a string is a palindrome",
        "variants": {
            "basic": {
                "description": "Case-insensitive palindrome check (ignores spaces)",
                "template": (
                    "def is_palindrome(s):\n"
                    "    \"\"\"Return True if s is a palindrome (ignores spaces and case).\"\"\"\n"
                    "    filtered = ''.join(ch.lower() for ch in s if not ch.isspace())\n"
                    "    return filtered == filtered[::-1]\n\n"
                    "# Example usage:\n"
                    "print(is_palindrome({user_s}))\n"
                )
            }
        },
        "inputs": [{"name": "user_s", "type": "str", "prompt": "Enter a string"}],
    },

    "fibonacci": {
        "display": "Fibonacci",
        "description": "Generate Fibonacci sequence up to n terms",
        "variants": {
            "iterative": {
                "description": "Iterative generator of n terms",
                "template": (
                    "def fibonacci(n):\n"
                    "    \"\"\"Return a list of first n Fibonacci numbers.\"\"\"\n"
                    "    if n <= 0:\n"
                    "        return []\n"
                    "    seq = [0]\n"
                    "    if n == 1:\n"
                    "        return seq\n"
                    "    seq.append(1)\n"
                    "    while len(seq) < n:\n"
                    "        seq.append(seq[-1] + seq[-2])\n"
                    "    return seq\n\n"
                    "# Example usage:\n"
                    "print(fibonacci({user_n}))\n"
                )
            }
        },
        "inputs": [{"name": "user_n", "type": "int", "prompt": "Enter number of terms (positive integer)"}],
    },

    "even_odd": {
        "display": "Even/Odd",
        "description": "Check if a number is even or odd",
        "variants": {
            "basic": {
                "description": "Modulo-based check",
                "template": (
                    "def is_even(n):\n"
                    "    \"\"\"Return True if n is even.\"\"\"\n"
                    "    return n % 2 == 0\n\n"
                    "# Example usage:\n"
                    "print('even' if is_even({user_n}) else 'odd')\n"
                )
            }
        },
        "inputs": [{"name": "user_n", "type": "int", "prompt": "Enter an integer"}],
    },
}


# -----------------------------
# Validators and helper functions
# -----------------------------

def prompt_input(prompt_text):
    """Read input and handle KeyboardInterrupt gracefully."""
    try:
        return input(f"{prompt_text}: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")
        sys.exit(0)


def get_typed_value(prompt_text, expected_type):
    """Prompt repeatedly until a value of expected_type is provided.

    expected_type is 'int' or 'str'. Returns a Python value.
    """
    while True:
        raw = prompt_input(prompt_text)
        if raw.lower() == "exit":
            print("Goodbye!")
            sys.exit(0)
        if expected_type == "int":
            try:
                return int(raw)
            except ValueError:
                print("Please enter a valid integer (or type 'exit').")
        else:  # string
            if raw == "":
                print("Please enter a non-empty string (or type 'exit').")
            else:
                return raw


def choose_variant(variants):
    """If multiple variants exist, let user choose; otherwise, return the single key."""
    keys = list(variants.keys())
    if len(keys) == 1:
        return keys[0]
    print("Choose implementation variant:")
    for i, k in enumerate(keys, 1):
        print(f"  {i}) {k} - {variants[k]['description']}")
    while True:
        choice = prompt_input("Enter variant number")
        if choice.isdigit() and 1 <= int(choice) <= len(keys):
            return keys[int(choice) - 1]
        print("Invalid selection; please enter the variant number.")


def format_template(template, mapping):
    """Format template by substituting mapping keys. Values should already be stringified appropriately."""
    try:
        return template.format(**mapping)
    except Exception as e:
        raise RuntimeError(f"Template formatting failed: {e}")


def display_code(code_str):
    sep = "=" * 60
    print(f"\n{sep}\nGenerated code:\n{sep}\n")
    print(code_str)
    print(sep)
    # Quick syntax check
    try:
        compile(code_str, "<string>", "exec")
        print("\n[Syntax check: OK]\n")
    except SyntaxError as se:
        print(f"\n[SyntaxError] {se}\n")


def save_code_to_file(code_str, default_name="generated_code.py"):
    """Prompt user for a filename and save the code to that file if confirmed."""
    while True:
        ans = prompt_input("Save generated code to file? (y/n)")
        if ans.lower() in ("y", "yes"):
            fname = prompt_input(f"Enter filename (default: {default_name})")
            if fname == "":
                fname = default_name
            try:
                with open(fname, "w", encoding="utf-8") as f:
                    f.write(code_str)
                print(f"Saved to {fname}")
            except Exception as e:
                print(f"Failed to save file: {e}")
            return
        if ans.lower() in ("n", "no"):
            return
        print("Please answer 'y' or 'n'.")


# -----------------------------
# CLI functions
# -----------------------------

def display_menu():
    print("\n=== Code Generator Bot ===")
    print("Type 'exit' at any prompt to quit.\n")
    keys = list(PROGRAMS.keys())
    for i, k in enumerate(keys, 1):
        print(f"{i}) {PROGRAMS[k]['display']} - {PROGRAMS[k]['description']}")
    return keys


def select_program():
    keys = display_menu()
    while True:
        choice = prompt_input("Select program by number or name")
        if choice.lower() == "exit":
            print("Goodbye!")
            sys.exit(0)
        # number
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(keys):
                return keys[idx]
        # name
        norm = choice.strip().lower()
        for k in keys:
            if k.lower() == norm or PROGRAMS[k]['display'].lower() == norm:
                return k
        print("Invalid selection; enter a valid number or program name.")


def collect_inputs(program_key):
    prog = PROGRAMS[program_key]
    collected = {}
    for inp in prog.get("inputs", []):
        name = inp["name"]
        typ = inp.get("type", "str")
        prompt = inp.get("prompt", name)
        val = get_typed_value(prompt, typ)
        # prepare representation for template substitution
        if typ == "str":
            collected[name] = repr(val)
        else:
            collected[name] = str(val)
    return collected


def generate_code(program_key, user_inputs):
    prog = PROGRAMS[program_key]
    variant_key = choose_variant(prog.get("variants", {}))
    template = prog["variants"][variant_key]["template"]
    code_str = format_template(template, user_inputs)
    return code_str


def main():
    while True:
        program_key = select_program()
        user_inputs = collect_inputs(program_key)
        code = generate_code(program_key, user_inputs)
        display_code(code)
        # Offer to save the generated code
        save_code_to_file(code)
        # Continue loop until exit


if __name__ == "__main__":
    main()

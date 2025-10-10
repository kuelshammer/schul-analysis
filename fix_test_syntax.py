#!/usr/bin/env python3
"""
Script to fix syntax issues in test assertions
"""

import re


def fix_test_syntax():
    with open("tests/test_arithmetik.py", "r") as f:
        content = f.read()

    # Fix missing multiplication signs
    # Pattern: numbers followed by variables without *
    fixes = [
        (r"(\d)([a-zA-Z])", r"\1*\2"),  # 2x -> 2*x
        (r"([a-zA-Z])(\d)", r"\1*\2"),  # x2 -> x*2
        (r"(\))([a-zA-Z])", r"\1*\2"),  # (x+1)x -> (x+1)*x
        (r"([a-zA-Z])(\()", r"\1*\2"),  # x(x+1) -> x*(x+1)
    ]

    # Only fix within assert_gleich calls
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if "assert_gleich(" in line:
            for pattern, replacement in fixes:
                # Only apply to the expected string argument
                if '"' in line:
                    # Find the string literal
                    parts = line.split('"')
                    if len(parts) >= 3:  # At least opening and closing quotes
                        # Fix the content inside quotes
                        for j in range(
                            1, len(parts) - 1, 2
                        ):  # Only odd indices are inside quotes
                            parts[j] = re.sub(pattern, replacement, parts[j])
                        line = '"'.join(parts)
            lines[i] = line

    fixed_content = "\n".join(lines)

    with open("tests/test_arithmetik.py", "w") as f:
        f.write(fixed_content)

    print("Fixed syntax issues in test_arithmetik.py")


if __name__ == "__main__":
    fix_test_syntax()

#!/usr/bin/env python3
"""
Script to fix test assertions in test_arithmetik.py
"""

import re


def fix_test_file():
    with open("tests/test_arithmetik.py", "r") as f:
        content = f.read()

    # Pattern to match assertions like: assert ergebnis.term() == "expected", ...
    pattern = r'assert\s+(\w+)\.term\(\)\s*==\s*"([^"]+)"([^,]*)'

    def replace_match(match):
        var_name = match.group(1)
        expected = match.group(2)
        optional_part = match.group(3) or ""

        # Keep the comment if it exists
        if optional_part.strip():
            return f'assert_gleich({var_name}.term(), "{expected}")  # {optional_part.strip()}'
        else:
            return f'assert_gleich({var_name}.term(), "{expected}")'

    # Apply the replacement
    fixed_content = re.sub(pattern, replace_match, content)

    # Handle special cases
    special_cases = [
        r'assert\s+(\w+)\.term\(\)\.replace\(" ", ""\)\s*==\s*"([^"]+)"([^,]*)',
        r'assert\s+(\w+)\.term\(\)\s*==\s*"([^"]+)"\s*or\s*\1\.term\(\)\s*==\s*"([^"]+)"',
    ]

    # First special case: .replace(" ", "")
    def replace_replace_match(match):
        var_name = match.group(1)
        expected = match.group(2)
        optional_part = match.group(3) or ""

        # For this case, we need to modify the expected value to include spaces
        # or remove spaces from the actual result
        return f'# Note: This test uses .replace(" ", "") - consider updating expected value\n    result = {var_name}.term().replace(" ", "")\n    assert result == "{expected}"'

    fixed_content = re.sub(special_cases[0], replace_replace_match, fixed_content)

    # Write the fixed content back
    with open("tests/test_arithmetik.py", "w") as f:
        f.write(fixed_content)

    print("Fixed test_arithmetik.py")


if __name__ == "__main__":
    fix_test_file()

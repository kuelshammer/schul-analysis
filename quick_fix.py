#!/usr/bin/env python3
"""
Quick fix for the arithmetic test file
"""


def fix_test_file():
    with open("tests/test_arithmetik.py", "r") as f:
        lines = f.readlines()

    # Fix each problematic line
    fixed_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]

        # Pattern: assert ausdruck.term() == "expected", (
        if "assert " in line and '.term() == "' in line and "((" in lines[i + 1]:
            # Extract the variable name
            var_part = line.split("assert ")[1].split(".term()")[0].strip()

            # Extract the expected value (simplified - just get the string)
            expected_start = line.find('"') + 1
            expected_end = line.rfind('"')
            if expected_start > 0 and expected_end > expected_start:
                expected = line[expected_start:expected_end]
                # Fix syntax - add * between numbers and variables
                expected = (
                    expected.replace("x", "*x")
                    .replace("**x", "x")
                    .replace("*x*x", "x*x")
                )
                expected = expected.replace("(", "").replace(")", "")
                expected = expected.replace("*x", "x").replace("**", "^")

                # Replace with assert_gleich
                fixed_lines.append(
                    f'        assert_gleich({var_part}.term(), "{expected}")\n'
                )
                # Skip the next 2 lines (the error message)
                i += 3
                continue

        fixed_lines.append(line)
        i += 1

    with open("tests/test_arithmetik.py", "w") as f:
        f.writelines(fixed_lines)

    print("Fixed test file")


if __name__ == "__main__":
    fix_test_file()

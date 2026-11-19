"""
utils.py
--------
Reusable helper functions for reading and validating user input.

Every input in the program goes through these functions, so invalid
input (letters instead of numbers, out-of-range values, empty names)
is handled in ONE place instead of being repeated everywhere.
"""


def print_header(title):
    """Print a section title surrounded by lines, for a tidy interface."""
    print("\n" + "-" * 50)
    print(f"{title:^50}")
    print("-" * 50)


def get_int_input(prompt, min_value=None, max_value=None):
    """
    Keep asking until the user enters a whole number within the range.
    Uses try/except to catch ValueError when the input is not a number.
    """
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("  [!] Invalid input. Please enter a whole number.")
            continue  # ask again

        if min_value is not None and value < min_value:
            print(f"  [!] Value must be at least {min_value}.")
        elif max_value is not None and value > max_value:
            print(f"  [!] Value must not be more than {max_value}.")
        else:
            return value


def get_non_empty_string(prompt):
    """Keep asking until the user types something that is not blank."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("  [!] This field cannot be empty.")


def get_yes_no(prompt):
    """Ask a yes/no question. Returns True for yes and False for no."""
    while True:
        answer = input(prompt + " (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  [!] Please answer 'y' or 'n'.")

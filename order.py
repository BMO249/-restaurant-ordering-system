"""
order.py
--------
Manages the customer's current order (the "cart").

The order is stored as a dictionary:   item code -> quantity
Example: {"F1": 2, "D1": 3} means 2 x Nasi Lemak Ayam and 3 x Teh Tarik.

Storing only the code and quantity (not a copy of the name and price)
keeps the data small and makes the menu the single source of truth.
"""

from menu import get_item

MAX_QTY_PER_ITEM = 50  # Business rule: stops typing mistakes such as 500


def create_order():
    """Return a new, empty order."""
    return {}


def add_item(order, code, quantity):
    """
    Add a quantity of an item to the order.
    If the item is already in the order, the quantity is increased.
    Returns (True, message) on success or (False, message) on failure.
    """
    code = code.strip().upper()
    item = get_item(code)

    # Decision making: validate before changing the order.
    if item is None:
        return False, f"Item code '{code}' does not exist."
    if quantity <= 0:
        return False, "Quantity must be greater than zero."

    current_qty = order.get(code, 0)
    if current_qty + quantity > MAX_QTY_PER_ITEM:
        return False, (f"Maximum {MAX_QTY_PER_ITEM} per item. "
                       f"You already have {current_qty}.")

    order[code] = current_qty + quantity
    return True, f"Added {quantity} x {item['name']}."


def remove_item(order, code, quantity):
    """
    Remove a quantity of an item from the order.
    If the quantity reaches zero, the item is deleted from the order.
    Returns (True, message) on success or (False, message) on failure.
    """
    code = code.strip().upper()

    if code not in order:
        return False, f"Item '{code}' is not in your order."
    if quantity <= 0:
        return False, "Quantity must be greater than zero."
    if quantity > order[code]:
        return False, f"You only have {order[code]} of this item."

    order[code] -= quantity
    name = get_item(code)["name"]
    if order[code] == 0:
        del order[code]
        return True, f"Removed {name} from your order."
    return True, f"Removed {quantity} x {name}. {order[code]} left."


def get_order_lines(order):
    """
    Convert the order into a list of dictionaries that are easy to print:
    [{"code", "name", "price", "qty", "line_total"}, ...]
    """
    lines = []
    for code, qty in order.items():
        item = get_item(code)
        lines.append({
            "code": code,
            "name": item["name"],
            "price": item["price"],
            "qty": qty,
            "line_total": item["price"] * qty,
        })
    return lines


def display_order(order):
    """Print the current order as a table."""
    if not order:
        print("\n  Your order is empty.")
        return

    print(f"\n  {'Code':<5} {'Item':<26} {'Qty':>4} {'Price':>8} {'Total':>9}")
    print("  " + "-" * 56)
    for line in get_order_lines(order):
        print(f"  {line['code']:<5} {line['name']:<26} {line['qty']:>4} "
              f"{line['price']:>8.2f} {line['line_total']:>9.2f}")
    print("  " + "-" * 56)

"""
main.py
-------
Restaurant Ordering System - entry point.

Run with:   python main.py

This file only controls the program flow (the menu-driven interface).
The real work is done by the other modules:
    menu.py     - menu data and display
    order.py    - adding / removing items
    billing.py  - bill calculation and receipts
    utils.py    - input validation helpers
"""

import menu
import order as order_module
import billing
from utils import print_header, get_int_input, get_non_empty_string, get_yes_no

# Record of every completed order during this session.
# Each entry is a dictionary: {"order_no", "customer", "total"}
sales_history = []


def show_main_menu():
    """Display the main menu options."""
    print_header("CITY BITES RESTAURANT - ORDERING SYSTEM")
    print("  1. View Menu")
    print("  2. Add Item to Order")
    print("  3. Remove Item from Order")
    print("  4. View Current Order")
    print("  5. Checkout & Print Receipt")
    print("  6. View Today's Sales Summary")
    print("  7. Exit")


def handle_add(current_order):
    """Ask for an item code and quantity, then add it to the order."""
    menu.display_menu()
    code = get_non_empty_string("Enter item code (e.g. F1): ")
    if not menu.is_valid_code(code):
        print(f"  [!] '{code}' is not on the menu.")
        return
    qty = get_int_input("Enter quantity: ", min_value=1,
                        max_value=order_module.MAX_QTY_PER_ITEM)
    success, message = order_module.add_item(current_order, code, qty)
    print(("  [OK] " if success else "  [!] ") + message)


def handle_remove(current_order):
    """Ask which item to remove and how many."""
    if not current_order:
        print("\n  Your order is empty. Nothing to remove.")
        return
    order_module.display_order(current_order)
    code = get_non_empty_string("Enter item code to remove: ")
    qty = get_int_input("Quantity to remove: ", min_value=1)
    success, message = order_module.remove_item(current_order, code, qty)
    print(("  [OK] " if success else "  [!] ") + message)


def handle_checkout(current_order):
    """
    Finish the order: ask for customer details, show the bill and receipt,
    save it, and record the sale. Returns True if checkout completed.
    """
    if not current_order:
        print("\n  [!] Cannot checkout an empty order. Please add items first.")
        return False

    print_header("CHECKOUT")
    order_module.display_order(current_order)
    customer = get_non_empty_string("Customer name: ")

    print("  Order type: 1 = Dine-in   2 = Take-away")
    order_type = get_int_input("Choose order type: ", min_value=1, max_value=2)
    dine_in = order_type == 1
    if dine_in:
        table = get_int_input("Table number (1-30): ", min_value=1, max_value=30)
        table_or_type = f"Dine-in, Table {table}"
    else:
        table_or_type = "Take-away"

    order_no = len(sales_history) + 1001  # simple running order number
    lines, bill = billing.build_receipt(current_order, customer,
                                        table_or_type, dine_in, order_no)

    if not get_yes_no(f"Confirm payment of RM {bill['total']:.2f}?"):
        print("  Checkout cancelled. Your order is kept.")
        return False

    print()
    print("\n".join(lines))

    filename = billing.save_receipt(lines, order_no)
    if filename:
        print(f"\n  Receipt saved as {filename}")

    sales_history.append({"order_no": order_no, "customer": customer,
                          "total": bill["total"]})
    return True


def show_sales_summary():
    """Show all orders completed during this session and the total sales."""
    print_header("TODAY'S SALES SUMMARY")
    if not sales_history:
        print("  No orders completed yet.")
        return
    for sale in sales_history:
        print(f"  Order {sale['order_no']}  {sale['customer']:<20} "
              f"RM {sale['total']:>8.2f}")
    total_sales = sum(sale["total"] for sale in sales_history)
    print("  " + "-" * 40)
    print(f"  Orders: {len(sales_history)}    Total sales: RM {total_sales:.2f}")


def main():
    """Main program loop: show the menu and act on the user's choice."""
    current_order = order_module.create_order()

    while True:
        show_main_menu()
        choice = get_int_input("Select an option (1-7): ", min_value=1, max_value=7)

        if choice == 1:
            menu.display_menu()
        elif choice == 2:
            handle_add(current_order)
        elif choice == 3:
            handle_remove(current_order)
        elif choice == 4:
            print_header("CURRENT ORDER")
            order_module.display_order(current_order)
        elif choice == 5:
            if handle_checkout(current_order):
                current_order = order_module.create_order()  # start fresh
        elif choice == 6:
            show_sales_summary()
        elif choice == 7:
            if current_order and not get_yes_no("You have an unpaid order. Exit anyway?"):
                continue
            print("\n  Thank you for using City Bites Ordering System. Goodbye!")
            break


# Only run main() when this file is executed directly, not when imported.
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n  Program stopped by user. Goodbye!")

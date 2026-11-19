"""
menu.py
-------
Stores the restaurant menu and provides functions to display it and
look up items.

Computational Thinking:
- Abstraction: each menu item is reduced to only what the program needs
  (code, name, price, category). Details such as recipe or ingredients
  are left out.
- Pattern Recognition: every item follows the same dictionary structure,
  so one loop can display the whole menu.
"""

# The menu is a dictionary: item code -> item details (another dictionary).
# Using a short code (e.g. "F1") makes it fast and easy for users to choose.
MENU = {
    # ----- Main Food -----
    "F1": {"name": "Nasi Lemak Ayam",       "price": 12.50, "category": "Food"},
    "F2": {"name": "Mee Goreng Mamak",      "price": 9.00,  "category": "Food"},
    "F3": {"name": "Chicken Chop",          "price": 18.90, "category": "Food"},
    "F4": {"name": "Roti Canai (2 pcs)",    "price": 4.00,  "category": "Food"},
    "F5": {"name": "Nasi Goreng Kampung",   "price": 10.50, "category": "Food"},
    # ----- Drinks -----
    "D1": {"name": "Teh Tarik",             "price": 3.50,  "category": "Drinks"},
    "D2": {"name": "Milo Ais",              "price": 4.50,  "category": "Drinks"},
    "D3": {"name": "Fresh Orange Juice",    "price": 7.00,  "category": "Drinks"},
    "D4": {"name": "Mineral Water",         "price": 2.00,  "category": "Drinks"},
    # ----- Desserts -----
    "S1": {"name": "Cendol",                "price": 6.00,  "category": "Dessert"},
    "S2": {"name": "ABC (Air Batu Campur)", "price": 6.50,  "category": "Dessert"},
    "S3": {"name": "Chocolate Lava Cake",   "price": 11.00, "category": "Dessert"},
}

# Order in which categories are shown on screen.
CATEGORIES = ["Food", "Drinks", "Dessert"]


def display_menu():
    """Print the full menu grouped by category."""
    print("\n" + "=" * 50)
    print(f"{'RESTAURANT MENU':^50}")
    print("=" * 50)

    # Outer loop: go through each category.
    for category in CATEGORIES:
        print(f"\n--- {category} ---")
        # Inner loop: print every item that belongs to this category.
        for code, item in MENU.items():
            if item["category"] == category:
                print(f"  [{code}] {item['name']:<28} RM {item['price']:>6.2f}")
    print("=" * 50)


def get_item(code):
    """
    Return the menu item for the given code, or None if it does not exist.
    The code is converted to upper case so 'f1' and 'F1' both work.
    """
    return MENU.get(code.strip().upper())


def is_valid_code(code):
    """Return True if the code exists on the menu."""
    return get_item(code) is not None

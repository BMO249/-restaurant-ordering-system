# City Bites – Restaurant Ordering System

A menu-driven, command-line restaurant ordering system written in Python.
Developed for **BIT2083/BIT1054/BCS2013 Fundamental of Computational Thinking (Python) – Assignment 2**, City University Malaysia.

## Features
- View the menu grouped by category (Food, Drinks, Dessert)
- Add items to an order by item code (e.g. `F1`) and quantity
- Remove items or reduce quantities
- View the current order with line totals
- Checkout for **Dine-in** (with table number) or **Take-away**
- Automatic bill calculation:
  - 10% discount when the subtotal is RM 100 or more
  - 10% service charge (dine-in only)
  - 6% service tax
- Prints a receipt and saves it as `receipt_<order no>.txt`
- Sales summary of all orders completed in the session
- Input validation on every prompt (no crashes on wrong input)

## Requirements
- Python 3.8 or newer (no external libraries needed)

## How to Run
```bash
git clone <your-repo-url>
cd restaurant-ordering-system
python main.py
```

## User Guide
| Option | What it does |
|---|---|
| 1. View Menu | Shows all items, codes and prices |
| 2. Add Item to Order | Enter an item code (e.g. `F1`) then a quantity (1–50) |
| 3. Remove Item from Order | Enter the code and how many to remove |
| 4. View Current Order | Shows items, quantities and line totals |
| 5. Checkout & Print Receipt | Enter customer name, choose Dine-in/Take-away, confirm payment |
| 6. View Today's Sales Summary | Lists completed orders and total sales |
| 7. Exit | Quits (asks for confirmation if an order is unpaid) |

## Project Structure
| File | Responsibility |
|---|---|
| `main.py` | Program entry point and menu-driven interface (controls the flow) |
| `menu.py` | Menu data (dictionary) and functions to display / look up items |
| `order.py` | Add, remove and display items in the current order |
| `billing.py` | Bill calculation, receipt building and saving |
| `utils.py` | Reusable input-validation helpers |

## Bill Calculation Algorithm
```
subtotal       = Σ (price × quantity)
discount       = 10% × subtotal          if subtotal ≥ RM 100, else 0
service charge = 10% × (subtotal − discount)        (dine-in only)
service tax    = 6%  × (subtotal − discount + service charge)
grand total    = subtotal − discount + service charge + service tax
```

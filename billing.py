"""
billing.py
----------
Calculates the bill and prints / saves the receipt.

Bill calculation algorithm:
    1. subtotal        = sum of (price x quantity) for every item
    2. discount        = 10% of subtotal if subtotal >= RM 100, else 0
    3. service charge  = 10% of (subtotal - discount)   [dine-in only]
    4. service tax     = 6%  of (subtotal - discount + service charge)
    5. grand total     = subtotal - discount + service charge + service tax
"""

from datetime import datetime
from order import get_order_lines

# Rates are constants so they can be changed in one place.
SERVICE_CHARGE_RATE = 0.10
SERVICE_TAX_RATE = 0.06
DISCOUNT_RATE = 0.10
DISCOUNT_THRESHOLD = 100.00


def calculate_bill(order, dine_in=True):
    """Return a dictionary with every part of the bill, rounded to 2 decimals."""
    # Each amount is rounded to 2 decimals (sen) as soon as it is calculated,
    # so the printed lines on the receipt always add up to the grand total.
    subtotal = round(sum(line["line_total"] for line in get_order_lines(order)), 2)

    # Decision: the discount only applies to big orders.
    if subtotal >= DISCOUNT_THRESHOLD:
        discount = round(subtotal * DISCOUNT_RATE, 2)
    else:
        discount = 0.0
    after_discount = subtotal - discount

    # Decision: take-away customers do not pay a service charge.
    service_charge = round(after_discount * SERVICE_CHARGE_RATE, 2) if dine_in else 0.0
    service_tax = round((after_discount + service_charge) * SERVICE_TAX_RATE, 2)
    total = round(after_discount + service_charge + service_tax, 2)

    return {
        "subtotal": subtotal,
        "discount": discount,
        "service_charge": service_charge,
        "service_tax": service_tax,
        "total": total,
    }


def build_receipt(order, customer, table_or_type, dine_in, order_no):
    """Build the receipt as a list of text lines (used for screen and file)."""
    bill = calculate_bill(order, dine_in)
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    text = [
        "=" * 50,
        f"{'CITY BITES RESTAURANT':^50}",
        f"{'Official Receipt':^50}",
        "=" * 50,
        f"Order No : {order_no}",
        f"Date     : {now}",
        f"Customer : {customer}",
        f"Type     : {table_or_type}",
        "-" * 50,
        f"{'Item':<26}{'Qty':>4}{'Price':>9}{'Total':>11}",
        "-" * 50,
    ]
    for line in get_order_lines(order):
        text.append(f"{line['name']:<26}{line['qty']:>4}{line['price']:>9.2f}"
                    f"{line['line_total']:>11.2f}")
    text.append("-" * 50)
    text.append(f"{'Subtotal':<36}RM {bill['subtotal']:>9.2f}")
    if bill["discount"] > 0:
        text.append(f"{'Discount (10%)':<36}RM {-bill['discount']:>9.2f}")
    if dine_in:
        text.append(f"{'Service Charge (10%)':<36}RM {bill['service_charge']:>9.2f}")
    text.append(f"{'Service Tax (6%)':<36}RM {bill['service_tax']:>9.2f}")
    text.append("=" * 50)
    text.append(f"{'GRAND TOTAL':<36}RM {bill['total']:>9.2f}")
    text.append("=" * 50)
    text.append(f"{'Thank you! Please come again.':^50}")
    return text, bill


def save_receipt(lines, order_no):
    """
    Save the receipt to a text file. Returns the file name, or None if
    saving failed (e.g. no permission), so the program does not crash.
    """
    filename = f"receipt_{order_no}.txt"
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write("\n".join(lines) + "\n")
        return filename
    except OSError as error:
        print(f"  [!] Could not save receipt: {error}")
        return None

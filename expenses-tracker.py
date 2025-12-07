#!/usr/bin/env python3
"""
Personal Expenses Tracker (expenses-tracker.py)
"""

import os
import sys
from datetime import datetime
from decimal import Decimal, InvalidOperation

BALANCE_FILE = "balance.txt"
EXPENSE_PREFIX = "expenses_"


# -------------------------------------------------
# Utility Functions
# -------------------------------------------------

def read_balance():
    """Reads balance from balance.txt or creates it if missing."""
    if not os.path.exists(BALANCE_FILE):
        with open(BALANCE_FILE, "w") as f:
            f.write("0.00")
        return Decimal("0.00")

    with open(BALANCE_FILE, "r") as f:
        raw = f.read().strip()
        try:
            return Decimal(raw)
        except InvalidOperation:
            print("Error: balance.txt is corrupted. Resetting to 0.00")
            with open(BALANCE_FILE, "w") as f:
                f.write("0.00")
            return Decimal("0.00")


def write_balance(amount):
    """Writes updated balance to balance.txt."""
    with open(BALANCE_FILE, "w") as f:
        f.write(f"{amount:.2f}")


def format_currency(value):
    return f"{value:.2f}"


def list_expense_files():
    return sorted(
        f for f in os.listdir(".")
        if f.startswith(EXPENSE_PREFIX) and f.endswith(".txt")
    )


def total_expenses_to_date():
    total = Decimal("0.00")

    for file in list_expense_files():
        with open(file, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 4:
                    try:
                        total += Decimal(parts[3])
                    except InvalidOperation:
                        pass

    return total


def available_balance():
    return read_balance() - total_expenses_to_date()


# -------------------------------------------------
# Feature 1: Main Menu
# -------------------------------------------------

def show_main_menu():
    print("\n=== Personal Expenses Tracker ===")
    print("1. Check Remaining Balance")
    print("2. View Expenses")
    print("3. Add New Expense")
    print("4. Exit")


# -------------------------------------------------
# Feature 2: Check Balance
# -------------------------------------------------

def check_remaining_balance():
    current = read_balance()
    spent = total_expenses_to_date()
    available = current - spent

    print("\n--- Balance Report ---")
    print(f"Initial/Current Balance : {format_currency(current)}")
    print(f"Total Expenses to Date : {format_currency(spent)}")
    print(f"Available Balance      : {format_currency(available)}")

    add = input("Add money to balance? (y/n): ").strip().lower()
    if add == "y":
        amount_str = input("Enter amount: ").strip()

        try:
            amount = Decimal(amount_str)
            if amount <= 0:
                print("Amount must be positive.")
                return
        except InvalidOperation:
            print("Invalid number entered.")
            return

        new_balance = current + amount
        write_balance(new_balance)
        print(f"Balance updated! New balance: {format_currency(new_balance)}")


# -------------------------------------------------
# Feature 3: Add Expense
# -------------------------------------------------

def add_new_expense():
    print("\n--- Add New Expense ---")
    available = available_balance()
    print(f"Available Balance: {format_currency(available)}")

    # 1. Date input
    date_str = input("Enter date (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return

    # 2. Item name
    item = input("Item name: ").strip()
    if item == "":
        print("Item name cannot be empty.")
        return

    # 3. Amount
    amount_str = input("Amount paid: ").strip()
    try:
        amount = Decimal(amount_str)
        if amount <= 0:
            print("Amount must be positive.")
            return
    except InvalidOperation:
        print("Invalid amount.")
        return

    # Confirmation
    print("\nPlease confirm:")
    print(f"Date   : {date_str}")
    print(f"Item   : {item}")
    print(f"Amount : {format_currency(amount)}")

    confirm = input("Save expense? (y/n): ").strip().lower()
    if confirm != "y":
        print("Cancelled.")
        return

    if amount > available:
        print("Insufficient balance! Cannot save expense.")
        return

    # File name
    filename = f"{EXPENSE_PREFIX}{date_str}.txt"

    # Expense ID
    next_id = 1
    if os.path.exists(filename):
        with open(filename, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
            if lines:
                last_id = int(lines[-1].split("|")[0])
                next_id = last_id + 1

    # Write entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{next_id}|{timestamp}|{item}|{amount:.2f}\n"

    with open(filename, "a") as f:
        f.write(entry)

    # Update balance
    new_balance = read_balance() - amount
    write_balance(new_balance)

    print("Expense saved successfully!")
    print(f"New balance: {format_currency(new_balance)}")


# -------------------------------------------------
# Feature 4: View Expenses
# -------------------------------------------------

def view_expenses():
    while True:
        print("\n--- View Expenses ---")
        print("1. Search by Item Name")
        print("2. Search by Amount")
        print("3. Back")

        choice = input("Choose option: ").strip()

        if choice == "1":
            query = input("Enter item name: ").lower().strip()
            results = []

            for file in list_expense_files():
                with open(file, "r") as f:
                    for line in f:
                        parts = line.strip().split("|")
                        if len(parts) == 4 and query in parts[2].lower():
                            results.append((file, parts))

            if not results:
                print("No matches found.")
            else:
                print(f"\nFound {len(results)} results:")
                for file, p in results:
                    print(f"{file} -> ID:{p[0]} Time:{p[1]} Item:{p[2]} Amount:{p[3]}")

        elif choice == "2":
            amt_str = input("Enter amount: ").strip()
            try:
                amt = Decimal(amt_str)
            except InvalidOperation:
                print("Invalid amount.")
                continue

            results = []
            for file in list_expense_files():
                with open(file, "r") as f:
                    for line in f:
                        parts = line.strip().split("|")
                        if len(parts) == 4 and Decimal(parts[3]) == amt:
                            results.append((file, parts))

            if not results:
                print("No results found.")
            else:
                print(f"\nFound {len(results)} results:")
                for file, p in results:
                    print(f"{file} -> ID:{p[0]} Time:{p[1]} Item:{p[2]} Amount:{p[3]}")

        elif choice == "3":
            return
        else:
            print("Invalid option.")


# -------------------------------------------------
# Main Program Loop
# -------------------------------------------------

def main():
    while True:
        show_main_menu()
        choice = input("Select option: ").strip()

        if choice == "1":
            check_remaining_balance()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            add_new_expense()
        elif choice == "4":
            print("Exiting... Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Enter 1–4.")


if __name__ == "__main__":
    main()


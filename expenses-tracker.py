#!/usr/bin/env python3


print(f'Expense saved successfully. Remaining balance (balance.txt): {format_currency(new_balance)}')




def view_expenses():
while  True:
print('\n--- View Expenses ---')
print('1. Search by item name')
print('2. Search by amount')
print('3. Back to main menu')
choice = input('Select option: ').strip()
if choice == '1':
query = input('Enter item name to search (case-insensitive substring): ').strip().lower()
if not query:
print('Search query cannot be empty.')
continue
results = []
for fname in list_expense_files():
with open(fname, 'r') as f:
for line in f:
if not line.strip():
continue
parts = line.strip().split('|')
if len(parts) >= 4 and query in parts[2].lower():
results.append((fname, parts))
if not results:
print('No matching expenses found.')
else:
print(f'Found {len(results)} matching entries:')
for fname, parts in results:
print(f'{fname} -> ID:{parts[0]} Time:{parts[1]} Item:{parts[2]} Amount:{parts[3]}')


elif choice == '2':
amt_str = input('Enter amount to search (exact amount): ').strip()
try:
amt = Decimal(amt_str)
except InvalidOperation:
print('Invalid amount.')
continue
results = []
for fname in list_expense_files():
with open(fname, 'r') as f:
for line in f:
if not line.strip():
continue
parts = line.strip().split('|')
if len(parts) >= 4:
try:
if Decimal(parts[3]) == amt:
results.append((fname, parts))
except InvalidOperation:
pass
if not results:
print('No matching expenses found.')
else:
print(f'Found {len(results)} matching entries:')
for fname, parts in results:
print(f'{fname} -> ID:{parts[0]} Time:{parts[1]} Item:{parts[2]} Amount:{parts[3]}')


elif choice == '3':
return
else:
print('Invalid choice. Please select 1-3.')


# ---------- Main loop ----------


def main():
while True:
show_main_menu()
choice = input('Select option: ').strip()
if choice == '1':
check_remaining_balance()
elif choice == '2':
view_expenses()
elif choice == '3':
add_new_expense()
elif choice == '4':
print('Saving data and exiting. Goodbye!')
# balance already persisted after changes
sys.exit(0)
else:
print('Invalid choice. Please select 1-4.')


if __name__ == '__main__':
main()

grocery_list ={}
budget = 0.0

def set_budget():
    global budget
    budget = float(input('Enter your total budget: '))
    print(f'Budget set to {budget}')

def add_item():
    item = input('Enter item name: ')
    quantity = int(input('Enter quantity: '))
    price = float(input('Enter price per unit: '))
    #add the items to the dictionary, key is item, values are quantity and price
    grocery_list[item] = (quantity, price)
    print(f'Added {item}')

def view_list():
    print('Your grocery list : ')
    #iterate through the dictionary to display the items
    for item, (qty, price) in grocery_list.items():
        print(f'{item}: {qty} @ {price} = {qty * price}')

def calculate_total():
    total = sum(qty*price for qty,price in grocery_list.values())
    print(f'Total cost : {total}')
    print(f'Remaining budget : {budget - total}')
    if total > budget:
        print('Warning!: You are over the budget')

def remove_item():
    item = input('Enter item to remove: ')
    if item in grocery_list:
        del grocery_list[item]
        print(f'{item} removed successfully')

    else:
        print('Item is not on the list')

def apply_discount():
    item = input('Enter item to be discounted: ')
    if item in grocery_list:
        discount = float(input('Enter discount %: '))
        qty, price = grocery_list[item]
        discounted_price = round(price *(1 - discount/100), 2)
        grocery_list[item] = (qty, discounted_price)
        print(f'New price for {item} : {discounted_price}')

def main():
    print('Welcome to the Smart Grocery List App')
    set_budget()
    while True:
        print(
            """
            1. Add item
            2. Remove item
            3. View list
            4. Calculate total
            5. Apply discount
            6. Exit 
            """
        )
        choice = input('Enter your choice(1-6): ')
        if choice == '1':
            add_item()

        elif choice == '2':
            remove_item()

        elif choice == '3':
            view_list()

        elif choice == '4':
            calculate_total()

        elif choice == '5':
            apply_discount()

        elif choice == '6':
            print('Exiting....')
            break
        else:
            print('Invalid choice')

main()

        
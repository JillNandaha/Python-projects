grocery_list = {}
budget = 0.0

#define functions for different action points
#0. Set budget 1.Add item. 2. View list. 3. Apply discount. 4. Calculate total. 5. Remove item. 6. Exit

def set_budget():
    global budget
    budget = float(input('Enter a set budget amount: '))
    print(f'The budget has been set to {budget}')

def add_item():
    
    item = input('Add an item : ')
    quantity = int(input('State the quantity of the item: '))
    price = float((input('State the unit price of the item: ')))
    #grocery_list = (f'{item} @ {price}, total is {quantity * price}')
    #create a dictionary for items, with quantity and price
    grocery_list[item] = (quantity,price)
    print(f'{item} has been added')

def view_list():
    print('Yourgrocery list: ')
    for item, (quantity, price) in grocery_list.items():
        print(f'{item}: {quantity} @ {price} = {quantity * price}')

def apply_discount():
    item = input('Enter item to be discounted: ')
    if item in grocery_list:
        discount = input('Enter % discount to be applied : ')
        quantity, price = grocery_list[item]
        discounted_price = round(price*(1-discount/100))
        grocery_list[item] = (quantity, discounted_price)
        print(f'New price for {item} is {discounted_price}')

def calculate_total():
    total = sum(quantity*price for quantity,price in grocery_list.values())
    print(f'Your total is {total}')
    print(f'Remaining amount is {budget - total}')
    if total > budget:
        print('Warning: You are above budget.')

def remove_item():
    item = input('Enter item to be romved : ')
    if item in grocery_list:
        del grocery_list[item]
        print(f'{item} has been removed.')

    else:
        print('The item is not in the grocery list')




def main():
    print('Welcome to you Smart Grocery Application')
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
        choice = input('Enter your choice (1-5): ')
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






contacts = []
def display_menu():
    print('\n -- Contact Book --')
    print('1. Add contact')
    print('2. View all contacts')
    print('3. Search contact')
    print('4. Exit')

#we use a set for the names because it does not allow duplicates
names_set = set()
def add_contact():
    name = input('Enter a name: ').strip().title()
    if name in names_set:
        print('Contact already exists')
        return
    phone = input('Enter phone number: ').strip()
    contact = {
        'name' : name,
        'phone' :phone
    }
    contacts.append(contact)
    names_set.add(name)
    print(f'{name} has been added to your contact list')

def view_contacts():
    if not contacts:
        print('No contacts to display')
        return
    print('\n -- All contacts --')
    for i, contact in enumerate(contacts, start=1):
        print(f'{i}. {contact["name"]} - {contact["phone"]}')

def search_contact():
    search_name = input('Enter a name to search: ').strip().title()
    found = False
    for contact in contacts:
        if contact["name"] == search_name:
            print(f'Found: {contact["name"]} - {contact["phone"]}')
            found = True
            break

    if not found:
        print('Contact not found')






while True:
    display_menu()
    choice = input('Enter an option(1-4): ')
    if choice == '1':
        add_contact()
    elif choice == '2':
        view_contacts()
    elif choice == '3':
        search_contact()
    elif choice == '4':
        print('Goodbye!')
        break
    else:
        print('Invalid choice. Please try again')


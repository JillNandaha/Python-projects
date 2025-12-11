with open('note.txt', 'r') as f:
    print("Current file contents:")
    print(f.read())


def add_note():
    note = input('Enter a note: ')
    with open('note.txt', 'a') as file:
        file.write(note + '\n')
    print('Note added succcessfully')

def view_notes():
    try:
        with open('note.txt', 'r') as file:
            notes = file.readlines()
            if notes:
                print('Your notes: ')
                for idx, note in enumerate(notes, 1):
                    print(f'{idx}. {note.strip()}')

            else:
                print('No notes found.')

    except FileNotFoundError:
        print('No such file found. Create the file first.')

def delete_note():
    view_notes()
    try:
        note_number = int(input('Enter the note number to be deleted: '))
        with open('note.txt', 'r') as file:
            notes = file.readlines()

        if 1 <= note_number <= len(notes):
            removed_note = notes.pop(note_number - 1)

            with open('note.txt', 'w') as file:
                file.writelines(notes)

            print(f'Deleted: {removed_note.strip()}')

        else:
            print('Invalid note number')


    except ValueError:
        print('Enter a valid number')

    except FileNotFoundError:
        print('There were no notes found')





def main():
    print('Welcome to the note taking app')

    while True:
        print(
            """
            *** NOTE TAKING APP ***
            1. Add note
            2. View notes
            3. Delete notes
            4. Exit
            """
        )
        choice = input('Select an option between  1 and 4: ')
        if choice == '1':
            add_note()

        elif choice == '2':
            view_notes()

        elif choice == '3':
            delete_note()

        elif choice == '4':
            print('Exiting...')
            break

        else:
            print('Invalid choice. Please try again.')

            

if __name__ == '__main__':
    main()
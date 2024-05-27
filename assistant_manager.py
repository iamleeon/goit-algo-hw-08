from address_book import AddressBook, Record
import pickle


def input_error(func):
    def inner(*args, **kwargs):
        help_message = "For mode details enter 'help'."
        value_error_message = ("Make sure you provided all needed arguments after a command. E.g in "
                               "'add username phone' a command should look like this: 'add Bob 0123456789'.\n"
                               f"{help_message}")
        index_error_value = ("Make sure you follow the 'phone username' template to display a contact's info.\n"
                             f"For example, 'phone Bob'.\n{help_message}")
        general_error_message = ("Seems like you've provided an invalid command.\n"
                                 f"{help_message}")
        try:
            return func(*args, **kwargs)
        except ValueError:
            return value_error_message
        except IndexError:
            return index_error_value
        except KeyError:
            return general_error_message
        except TypeError:
            return general_error_message
    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "The contact has been updated successfully."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "The contact has been added successfully."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    message = f"{name} is not in the contacts."
    if record is None:
        return message
    if old_phone:
        record.edit_phone(old_phone, new_phone)
        message = "The contact's phone has been changed successfully."
    return message


@input_error
def display_contact(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    message = f"{name} was not found."
    phones_list = list()
    if record is None:
        return message
    for item in record.phones:
        phones_list.append(item.value)
    message = f"Name: {name}. Phones: {', '.join(phone for phone in phones_list)}"
    return message


@input_error
def display_all_contacts(book: AddressBook):
    contacts_list = ""
    for key in book.keys():
        if key:
            contacts_list += f"{book[key]}\n"
        else:
            break
    return contacts_list


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    message = "The birthday was not added because the contact was not found."
    if record is None:
        return message
    else:
        record.add_birthday(birthday)
        message = "The birthday has been added successfully."
    return message


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    message = f"{name} was not found."
    if record is None:
        return message
    else:
        message = f"Name: {name}. Birthday: {record.birthday}"
    return message


@input_error
def birthdays(book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    message = "No upcoming birthdays in the following 7 days."
    if upcoming_birthdays:
        return upcoming_birthdays
    return message


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(book, file)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()


def main():
    book = load_data()
    instruction = (
        "Please use the instruction below:\n\n"
        "'add \x1B[3musername phone\x1B[0m' to add a new contact. "
        "A phone number should be 10-digit long. E.g. 'add Bob 0123456789'\n"
        "'change \x1B[3musername old_phone new_phone\x1B[0m' to update an existing contact (phone). "
        "A new phone number should be 10-digit long. E.g. 'change Bob 0987654321 1234567890'\n"
        "'phone \x1B[3musername\x1B[0m' to display a contact's info. E.g. 'phone Bob'\n"
        "'all' to display all contacts\n"
        "'add-birthday \x1B[3musername DD.MM.YYYY\x1B[0m' to add contacts' birthday. "
        "E.g. 'add-birthday Bob 22.05.2000'\n"
        "'show-birthday \x1B[3musername\x1B[0m' to see contacts' birthday. E.g. 'show-birthday Bob'\n"
        "'birthdays' to display all upcoming birthdays in the following 7 days\n"
        "'help' to see this instruction\n"
        "'close' or 'exit' to stop the assistant\n"
                   )
    print("Welcome to the assistant manager! My name is Alex.")    
    print(f"{instruction}")

    while True:
        user_input = input("Please enter a command: ")
        command, *args = parse_input(user_input)
        if command in ["exit", "close"]:
            save_data(book)
            print(f"Good bye!")
            break
        elif command in ["hello", "hi", "nice to meet you"]:
            print(f"How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(display_contact(args, book))
        elif command == "all":
            print(display_all_contacts(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        elif command == "help":
            print(f"{instruction}")
        else:
            print("Sorry, I didn't quite catch you. Seems like you've provided an invalid command.\n"
                  "Enter 'help' for the instructions.")


if __name__ == '__main__':
    main()
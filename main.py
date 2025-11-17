from addressbook import AddressBook
from record import Record
from fields import Name, Phone, Birthday
import pickle


def save_to_file(book, filename="addressbook.bin"):
    with open(filename, "wb") as f:
        pickle.dump(book.data, f)


def load_from_file(book, filename="addressbook.bin"):
    try:
        with open(filename, "rb") as f:
            book.data = pickle.load(f)
    except FileNotFoundError:
        book.data = {}


def input_error(func):
    def wrapper(book, args, *fargs, **fkwargs):
        try:
            return func(book, args, *fargs, **fkwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found"
        except IndexError:
            return "Not enough arguments"
    return wrapper


@input_error
def add_command(book, args):
    name, phone = args
    record = book.find(name)

    if not record:
        record = Record(Name(name))
        book.add_record(record)

    record.add_phone(Phone(phone))
    return "Phone added"


@input_error
def change_command(book, args):
    name, old, new = args
    record = book.find(name)
    record.edit_phone(old, new)
    return "Phone changed"


@input_error
def phone_command(book, args):
    name = args[0]
    record = book.find(name)
    return ", ".join(p.value for p in record.phones)


def show_all(book, args):
    if not book.data:
        return "No contacts"
    return "\n".join(str(r) for r in book.data.values())


@input_error
def add_birthday(book, args):
    name, bday = args
    record = book.find(name)
    if not record:
        raise KeyError("Contact not found")
    record.add_birthday(Birthday(bday))
    return "Birthday added"


@input_error
def show_birthday(book, args):
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError("Contact not found")
    if record.birthday:
        return record.birthday.value
    return "No birthday set"


def birthdays(book, args):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays"
    return "\n".join(f"{name}: {date}" for name, date in upcoming)


COMMANDS = {
    "add": add_command,
    "change": change_command,
    "phone": phone_command,
    "all": show_all,
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": birthdays,
}


def parse_command(user_input):
    parts = user_input.split()
    if not parts:
        raise IndexError("Empty command")
    cmd = parts[0]
    args = parts[1:]
    return cmd, args


def main():
    address_book = AddressBook()
    load_from_file(address_book)

    print("Assistant bot started!")

    while True:
        user_input = input(">>> ").strip()
        if not user_input:
            continue

        if user_input in ("exit", "close", "good bye"):
            save_to_file(address_book)
            print("Good bye!")
            break

        try:
            cmd, args = parse_command(user_input)
        except IndexError:
            print("Please enter a command.")
            continue

        handler = COMMANDS.get(cmd)
        if handler:
            result = handler(address_book, args)
            print(result)
        else:
            print("Unknown command")


if __name__ == "__main__":
    main()

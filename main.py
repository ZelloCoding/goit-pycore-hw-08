from addressbook import AddressBook
from record import Record
from fields import Name, Phone, Birthday


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found"
        except IndexError:
            return "Not enough arguments"
    return wrapper


address_book = AddressBook()


@input_error
def add_command(args):
    name, phone = args
    record = address_book.find(name)

    if not record:
        record = Record(Name(name))
        address_book.add_record(record)

    record.add_phone(Phone(phone))
    return "Phone added"


@input_error
def change_command(args):
    name, old, new = args
    record = address_book.find(name)
    record.edit_phone(old, new)
    return "Phone changed"


@input_error
def phone_command(args):
    name = args[0]
    record = address_book.find(name)
    return ", ".join(p.value for p in record.phones)


def show_all(args):
    if not address_book.data:
        return "No contacts"

    return "\n".join(str(r) for r in address_book.values())


@input_error
def add_birthday(args):
    name, bday = args
    record = address_book.find(name)
    record.add_birthday(Birthday(bday))
    return "Birthday added"


@input_error
def show_birthday(args):
    name = args[0]
    record = address_book.find(name)
    return record.birthday.value


def birthdays(args):
    upcoming = address_book.get_upcoming_birthdays()
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
    cmd = parts[0]
    args = parts[1:]
    return cmd, args


def main():
    print("Assistant bot started!")

    while True:
        user_input = input(">>> ")

        if user_input in ("exit", "close", "good bye"):
            print("Good bye!")
            break

        cmd, args = parse_command(user_input)

        if cmd in COMMANDS:
            print(COMMANDS[cmd](args))
        else:
            print("Unknown command")


if __name__ == "__main__":
    main()

import pickle
from collections import UserDict
from datetime import datetime
from record import Record
from fields import Name


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days=7):
        today = datetime.today().date()
        upcoming = []

        for record in self.data.values():
            if record.birthday:
                bday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                next_bday = bday.replace(year=today.year)

                if next_bday < today:
                    next_bday = next_bday.replace(year=today.year + 1)

                delta = (next_bday - today).days

                if 0 <= delta <= days:
                    upcoming.append((record.name.value, record.birthday.value))

        return upcoming

    # Методи для збереження та завантаження адресної книги
    def save_to_file(self, filename="addressbook.bin"):
        with open(filename, "wb") as f:
            pickle.dump(self.data, f)

    def load_from_file(self, filename="addressbook.bin"):
        try:
            with open(filename, "rb") as f:
                self.data = pickle.load(f)
        except FileNotFoundError:
            self.data = {}

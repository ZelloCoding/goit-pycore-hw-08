from datetime import datetime, timedelta
from fields import Name, Phone, Birthday


class Record:
    def __init__(self, name: Name):
        self.name = name
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def remove_phone(self, phone: str):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old, new):
        for p in self.phones:
            if p.value == old:
                p.value = new
                return
        raise ValueError("Old phone not found")

    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday

    def days_to_birthday(self):
        if not self.birthday:
            return None

        today = datetime.today()
        bday = datetime.strptime(self.birthday.value, "%d.%m.%Y")
        next_bday = datetime(today.year, bday.month, bday.day)

        if next_bday < today:
            next_bday = datetime(today.year + 1, bday.month, bday.day)

        return (next_bday - today).days

    def __str__(self):
        phones = ", ".join(p.value for p in self.phones)
        bday = self.birthday.value if self.birthday else "—"
        return f"{self.name.value}: {phones}; Birthday: {bday}"

from datetime import datetime
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone must contain 10 digits")
        self.__value = value


class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, date_str):
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Birthday must be in format DD.MM.YYYY")
        self.__value = date_str

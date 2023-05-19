import re
from collections import UserDict
from datetime import datetime, timedelta, date

class Field:
    pass

class Name(Field):
    def __init__(self, name):
        self.value = name

class Phone(Field):
    def __init__(self, phone):
        self.value = self.validate_phone(phone)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = self.validate_phone(new_value)

    def validate_phone(self, phone):
        phone_pattern = re.compile(r'^\+?\d{1,4}[-\.\s]?\(?\d{1,4}?\)?[-\.\s]?\d{1,4}[-\.\s]?\d{1,4}[-\.\s]?\d{1,9}$')
        if not phone_pattern.match(phone):
            raise ValueError("Invalid phone number format")
        return phone

class Birthday(Field):
    def __init__(self, birthday=None):
        if birthday is not None:
            self.value = self.validate_birthday(birthday)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = self.validate_birthday(new_value)

    @staticmethod
    def validate_birthday(birthday):
        if isinstance(birthday, date):
            return birthday
        if isinstance(birthday, Birthday):
            birthday = birthday.value
        try:
            date_object = datetime.strptime(str(birthday), '%Y-%m-%d').date()
            return date_object
        except ValueError:
            raise ValueError("Invalid date format. Please use the format 'YYYY-MM-DD'")


class Record:
    def __init__(self, name, phones=None, birthday=None):
        self.name = name
        self.phones = phones if phones is not None else []
        if birthday:
            self.birthday = Birthday(birthday)
        else:
            self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            next_birthday = self.birthday.value.replace(year=today.year)
            if today > next_birthday:
                next_birthday = next_birthday.replace(year=today.year + 1)
            return (next_birthday - today).days
        else:
            return None

class AddressBook(UserDict):
    def __init__(self, records_per_page=3):
        super().__init__()
        self.records_per_page = records_per_page

    def add_record(self, name, phones=None, birthday=None):
        record = Record(name, phones, birthday)
        self.data[record.name.value] = record

    def iterator(self):
        records = list(self.data.values())
        for i in range(0, len(records), self.records_per_page):
            yield records[i:i + self.records_per_page]

    def add_contact(name, phone, birthday=None):
        record = Record(name, [Phone(phone)], birthday)
        phone_book.add_record(name, [Phone(phone)], birthday)
        return f"Contact {name} has been added with phone number {phone}"




phone_book = AddressBook()

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found"
        except ValueError:
            return "Invalid input format. Please enter name and phone number separated by a space"
        except IndexError:
            return "Invalid command. Please try again"
    return inner

@input_error
def handle_input(command):
    return command.lower()

def add_contact(name, phone, birthday=None):
    if birthday:
        phone_book.add_record(Name(name), [Phone(phone)], Birthday(birthday))
    else:
        phone_book.add_record(Name(name), [Phone(phone)])
    return f"Contact {name} has been added with phone number {phone}"

def change_contact(name, current_phone, new_phone):
    if name in phone_book.data:
        phone_book.data[name].edit_phone(current_phone, new_phone)
        return f"Phone number for {name} has been updated to {new_phone}"
    else:
        return "Contact not found"

def find_contact(name):
    if name in phone_book.data:
        phones = ', '.join([phone.value for phone in phone_book.data[name].phones])
        birthday = phone_book.data[name].birthday.value if phone_book.data[name].birthday else "not set"
        return f"Phones: {phones}, Birthday: {birthday}"
    else:
        return "Contact not found"

def show_all_contacts():
    output = ""
    for name, record in phone_book.data.items():
        phones = ', '.join([phone.value for phone in record.phones])
        birthday = record.birthday.value if record.birthday else "not set"
        output += f"{name}: Phones - {phones}, Birthday - {birthday}\n"
    return output

def change_birthday(name, birthday):
    if name in phone_book.data:
        phone_book.data[name].birthday = Birthday(birthday)
        return f"Birthday for {name} has been updated to {birthday}"
    else:
        return "Contact not found"

def days_to_birthday(name):
    if name in phone_book.data:
        days = phone_book.data[name].days_to_birthday()
        if days is None:
            return f"No birthday information for {name}"
        else:
            return f"{days} days until {name}'s next birthday"
    else:
        return "Contact not found"

def show_paginated_contacts():
    iterator = phone_book.iterator()
    for chunk in iterator:
        output = ""
        for record in chunk:
            name = record.name.value
            phones = ', '.join([phone.value for phone in record.phones])
            output += f"{name}: {phones}\n"
        print(output)
        input("Press Enter to continue...")

def main():
    print("Hello! This CLI phone book assistant.")
    while True:
        command = input("> ")
        command = handle_input(command)
        if command == "hello":
            print("How can I help you?")
        elif command.startswith("add"):
            try:
                _, name, phone, birthday = command.split()
                print(add_contact(name, phone, birthday))
            except ValueError:
                print("Invalid input format. Please enter name, phone number, and optional birthday separated by a space")
        elif command.startswith("birthday"):
            try:
                _, name, birthday = command.split()
                print(change_birthday(name, birthday))
            except ValueError:
                print("Invalid input format. Please enter name and birthday separated by a space")
        elif command.startswith("days"):
            try:
                _, name = command.split()
                print(days_to_birthday(name))
            except ValueError:
                print("Invalid input format. Please enter name and command separated by a space")
        elif command == "show paginated":
            show_paginated_contacts()
        else:
            print("Invalid command. Please try again")

if __name__ == "__main__":
    main()
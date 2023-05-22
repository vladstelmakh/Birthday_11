

from datetime import date

class Field:
    def __init__(self, value=None):
        self._value = value

    def set_value(self, value):
        self._value = value

    def get_value(self):
        return self._value


class Phone(Field):
    def set_value(self, value):
       
        if self.is_valid_phone(value):
            super().set_value(value)
        else:
            raise ValueError("Invalid phone number")

    def is_valid_phone(self, value):
        
        return len(value) == 10 and value.isdigit()


class Birthday(Field):
    def set_value(self, value):
        
        if self.is_valid_birthday(value):
            super().set_value(value)
        else:
            raise ValueError("Wrong date of birth")

    def is_valid_birthday(self, value):
        
       
        return isinstance(value, date)

    def days_to_birthday(self):
        if self._value:
            today = date.today()
            next_birthday = date(today.year, self._value.month, self._value.day)
            if next_birthday < today:
                next_birthday = date(today.year + 1, self._value.month, self._value.day)
            return (next_birthday - today).days
        return None


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phone = Phone(phone)
        self.birthday = Birthday(birthday)


class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def remove_record(self, record):
        self.records.remove(record)

    def iterator(self, page_size):
        num_pages = (len(self.records) + page_size - 1) 
        for page in range(num_pages):
            start = page * page_size
            end = start + page_size
            yield self.records[start:end]

def main():

    
    record1 = Record("John Doe", "3434567895", date(1991, 5, 11))
    record2 = Record("Jane Smith", "1276543211", date(1982, 4, 20))
    record3 = Record("Bob Johnson")

    
    address_book = AddressBook()
    address_book.add_record(record1)
    address_book.add_record(record2)
    address_book.add_record(record3)

    
    for page in address_book.iterator(page_size=2):
        for record in page:
            print(record.name)

    print(record1.birthday.days_to_birthday())
if __name__ == '__main__':
    main()
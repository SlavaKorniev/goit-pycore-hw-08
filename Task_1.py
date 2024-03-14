from collections import UserDict
from datetime import datetime, timedelta
import pickle

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
       return str(self.value)

class Name(Field):
    # Клас для зберігання імені контакту. Обов'язкове поле.
		pass

class Phone(Field):
    # Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
    def __init__(self, value):
        self.value = self.phonevalid(value)       

    def phonevalid(self, numer):
        if len(numer) == 10:
            for count in numer:
                if count.isdigit():
                    okay = True
                else:
                    okay = False
                    break
        else:
            okay = False
        if okay:    
            return numer
        else:
            print ("Invalid phone format. Use ten numbers (XXXXXXXXXX)")
            return None
        
class Birthday(Field):
    # Клас для зберігання дня народження. Має перевірку формату  DD.MM.YYYY
    def __init__(self, value):
        try:
            # Додайте перевірку коректності даних
            # та перетворіть рядок на об'єкт datetime
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
                    
        except ValueError:
            self.value = None
            print ("Invalid date format. Use DD.MM.YYYY")

class Record:
    # Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів, день народження
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    def add_phone(self, phone):
        # метод для додавання об'єктів Phone
        self.phone = Phone(phone)   #obj
        if self.phone.value != None:
            self.phones.append(self.phone)

    def remove_phone(self, phone):
        # метод для видалення об'єктів Phone
        self.phone = phone      #str        
              
        for p in self.phones:
            if p.value == self.phone:
                self.phones.remove(p)

    def edit_phone (self, old_phone, new_phone):
        # метод для редагування об'єктів Phone
        self.old_phone = old_phone      # str
        self.new_phone = new_phone      # str
        
        for p in self.phones:
            if p.value == self.old_phone:
                p.value = self.new_phone

    def find_phone (self, fnd_phone):
        # метод для пошуку об'єктів Phone
        self.fnd_phone = fnd_phone      #str

        for p in self.phones:
            if p.value == self.fnd_phone:
                findet_phone = p.value
            else:
                findet_phone = None 

        return findet_phone

    def add_birthday (self, birthday):
        self.birthday = Birthday (birthday)
        if self.birthday.value == None:
            self.birthday = None


    
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

        
class AddressBook(UserDict):
    # реалізація класу
	
    def add_record(self, recording):
    # метод add_record, який додає запис до self.data
        self.key = recording.name.value
        self.value = recording
        self.data[self.key] = self.value

    def find(self, name_fnd):
    # метод find, який знаходить запис за ім'ям
        self.name_fnd = name_fnd
        return self.data.get(self.name_fnd)

    def delete(self, name_del):
    # метод delete, який видаляє запис за ім'ям
        self.name_del = name_del
        del self.data[self.name_del]

    
def input_error(func):
    '''Декоратор, обробляє винятки, що виникають у функціях (KeyError, ValueError, IndexError)'''
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter the argument for the command"
        except ValueError:
            return "Enter the argument for the command: [command] [name] [phone_numder]/[birthday]"
        except IndexError:
            return "Enter the argument for the command: [command] [name]"
        
    return inner

def parse_input(user_input):
    ''' Функція отримання команди і значення з командної строки'''
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return f"{message}  {record}"

@input_error
def change_contact(args, book: AddressBook):
    '''Функція змінює у пам'яті, (словнику), новий контакт'''
    name, phone_old, *_ = args
    record = book.find(name)
    if record is None:
        return f"No name in phone books. You can added name by command 'add'"
    
    if record.find_phone(phone_old):
        y_n_input = None
        phone_new = None
        while y_n_input != "y" and "n":
            y_n_input = input(f"A you realy want change Phone number '{name}': '{phone_old}'?  (Y/N)\n>>> ").lower()
            if y_n_input == "y":
                while phone_new is None:
                    phone_new = Phone(input("Enter new phone.\n>>> ")).value
                
                record.edit_phone (phone_old, phone_new)
                return f"Contact changed: {record}"
            elif y_n_input.lower() == "n":
                return f"Change canceled: {record}"
    else:
        return f"No Phone: {phone_old} in Contact :{name}. Try anoher phone"

@input_error        
def show_phone(args, book: AddressBook):
    '''Виводить у консоль номер телефону для зазначеного контакту'''
    name, *_ = args
    record = book.find(name)
    if record is None:
        return f"No name in phone books. You can added name by command 'add'"
    else:
        return f"Contact findet: {record}"
    
@input_error
def show_all(book: AddressBook):
    '''Виводить у консоль всі телефони зі словника'''
    all_text = "All contacts is:\n"
    for name, record in book.data.items():
        all_text = all_text + f"{record}\n"
    return all_text    

@input_error
def add_birthday(args, book: AddressBook):
    # додаємо до контакту день народження в форматі DD.MM.YYYY
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        return f"No name in phone books. You can added name by command 'add'"
    
    if record.birthday is None:
        record.add_birthday(birthday)
        if record.birthday is None:
            return f"No birthdays added"
        else:
            return f"{name}'s birthday: {record.birthday.value} added"
    else:
        old_data_birsday = record.birthday.value
        record.add_birthday(birthday)
        if record.birthday is None:
            return f"No birthdays added"
        else:
            return f"{name}'s birthday value: {old_data_birsday} changed on: {record.birthday.value}"
    
 

@input_error
def show_birthday(args, book: AddressBook):
    # показуємо день народження контакту
    name, *_ = args
    record = book.find(name)
    if record is None:
        return f"No name in phone books. You can added name by command 'add'"
    
    if record.birthday is None:
        return f"No birthday added in contacts name {name}"
    else:
        return f"{name}'s birthday is: {record.birthday.value}"
    


@input_error
def birthdays(book: AddressBook):
    # повертає список користувачів, яких потрібно привітати по днях на наступному тижні
    date_now_object = datetime.today().date()   #take date today
    year_now = date_now_object.year
    all_text_value = False
    all_text = ""
    for name, record in book.data.items():
               
        if record.birthday != None:
            # take data birthday from book
            date_user_birthday = record.birthday.value

            # change year in date_user on curently
            present_date_user_birthday = datetime(year=year_now, month=date_user_birthday.month, day=date_user_birthday.day).date()
            weekday_birsday = present_date_user_birthday.weekday()
            # congratulations day
            if weekday_birsday == 5:
                present_date_user_congratulations = present_date_user_birthday + timedelta(days=2)
            
            elif weekday_birsday == 6:
                present_date_user_congratulations = present_date_user_birthday + timedelta(days=1)        

            else:
                present_date_user_congratulations = present_date_user_birthday

            #find difference between users congratulations date and today
            date_user_delta = present_date_user_congratulations - date_now_object

            if 0<= date_user_delta.days <=7:            
                all_text_value = True
                all_text = all_text + f"{record}, Congratulations date: {present_date_user_congratulations}\n"

    if all_text_value:
        all_text = "Birsdays on next week is:\n" + all_text
    else:
        all_text = "There are no birsdays on next week\n"  

    return all_text
    
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено




def main():
    # Завантаження, або за відсутності, створення нової адресної книги \addressbook.pkl
    book = load_data()

    print("Welcome to the assistant bot!")
    commands = ["hello", "add", "change", "phone", "all", "add-birthday", "show-birthday", "birthdays", "close", "exit"]
    while True:
        user_input = input(f"Enter a command ({commands}): \n>>> ")
        command, *args = parse_input(user_input)

        if command in [commands [8], commands [9]]: #["close", "exit"]
            print("Good bye!")
            break

        elif command == commands [0]: # "hello":
            print("How can I help you?")

        elif command == commands [1]: # "add":
            print(add_contact(args, book))

        elif command == commands [2]: # "change":
            print(change_contact(args, book))
            
        elif command == commands [3]: # "phone":
            print(show_phone(args, book))
            
        elif command == commands [4]: # "all":
            print(show_all(book))
            
        elif command == commands [5]: # "add-birthday":
            print(add_birthday(args, book))
            
        elif command == commands [6]: # "show-birthday":
            print(show_birthday(args, book))

        elif command == commands [7]: # "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")

    save_data(book)  # Викликати перед виходом з програми

if __name__ == '__main__':
    main()

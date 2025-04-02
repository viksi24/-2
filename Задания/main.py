# 2.1

#1
J = "ab"
S = "aabbccd"

count = 0
for s in S:
    if s in J:
        count += 1

print(count)





#2
from itertools import combinations

def find_combinations(candidates, target):
    candidates.sort()
    result = set()

    for i in range(1, len(candidates) + 1):
        for combo in combinations(candidates, i):
            if sum(combo) == target:
                result.add(combo)

    return list(result)

candidates1 = [2, 5, 2, 1, 2]
target1 = 5
print(find_combinations(candidates1, target1))

candidates2 = [10, 1, 2, 7, 6, 1, 5]
target2 = 8
print(find_combinations(candidates2, target2))





#3
def repeat_check(nums):
    return len(nums) != len(set(nums))

print(repeat_check([1, 2, 3, 4]))
print(repeat_check([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]))
print(repeat_check([1, 2, 3, 1]))















#2.2

#1
class Student:
    def __init__(self, surname, date_of_birth, group_number, marks):
        self.surname = surname
        self.date_of_birth = date_of_birth
        self.group_number = group_number
        self.marks = marks

    def update_info(self, surname=None, date_of_birth=None, group_number=None):
        if surname:
            self.surname = surname
        if date_of_birth:
            self.date_of_birth = date_of_birth
        if group_number:
            self.group_number = group_number

    def display_info(self):
        print(f"Фамилия: {self.surname}")
        print(f"Дата рождения: {self.date_of_birth}")
        print(f"Номер группы: {self.group_number}")
        print(f"Успеваемость: {self.marks}")
        print()


class StudentNotFoundError(Exception):
    pass


students = [
    Student("Шумет", "2006-10-12", "641", [4, 5, 3, 4, 5]),
    Student("Волков", "2004-12-15", "631", [2, 2, 2, 2, 2]),
    Student("Бутонаева", "2007-03-31", "641", [3, 3, 4, 4, 3]),
    Student("Гудина", "2006-03-30", "641", [4, 5, 5, 4, 4]),
    Student("Никитина", "2006-11-30", "641", [5, 5, 5, 5, 5])
]

search_last_name = input("Введите фамилию: ").strip()
search_birth_date = input("Введите дату рождения (гггг-мм-дд): ").strip()

try:
    found = False
    for student in students:
        if student.surname == search_last_name and student.date_of_birth == search_birth_date:
            student.display_info()
            found = True

    if not found:
        raise StudentNotFoundError(f"Студент с фамилией '{search_last_name}' и датой рождения '{search_birth_date}' не найден.")

except StudentNotFoundError as e:
    print(f"Ошибка: {e}")








#2
class Train:
    def __init__(self, item_name, train_number, departure_time):
        self.item_name = item_name
        self.train_number = train_number
        self.departure_time = departure_time

    def display_info(self):
        return f"Поезд номер {self.train_number}\nНаправление: {self.item_name}\nВремя отправления: {self.departure_time}"

Тrains = [
    Train("Томск", 105, "12:30"),
    Train("Новосибирск", 17, "19:15"),
    Train("Рязань", 298, "15:35"),
    Train("Омск", 112, "22:00"),
    Train("Тюмень", 102, "00:45")
]

try:
    train_number_input = int(input("Введите номер поезда: "))

    train_found = False
    for train in Тrains:
        if train.train_number == train_number_input:
            print(train.display_info())
            train_found = True

    if not train_found:
        print("Поезд с таким номером не найден.")

except ValueError:
    print("Ошибка: введите правильный номер поезда ")



# 3код




#4
class Counter:
    def __init__(self, value=0):
        self.value = value

    def increase(self):
        self.value += 1

    def decrease(self):
        self.value -= 1

    def get_value(self):
        return self.value


try:
    start_value = input("Введите значение счетчика : ")

    start_value = int(start_value) if start_value.strip() else 0

    counter = Counter(start_value)

    print(f"Текущее значение счетчика: {counter.get_value()}")

    counter.increase()
    print(f"После увеличения: {counter.get_value()}")

    counter.decrease()
    print(f"После уменьшения: {counter.get_value()}")

except ValueError:
    print("Ошибка: введите целое число.")







#5

class NewClass:
    def __init__(self, value1=0, value2=0):
        self.value1 = value1
        self.value2 = value2
        print(f"Объект создан с value1 = {self.value1}, value2 = {self.value2}")

    def __del__(self):
        print(f"Объект с value1 = {self.value1}, value2 = {self.value2} удален.")

    def property_values(self):
        print(f"value1: {self.value1}, value2: {self.value2}")


try:
    obj1 = NewClass()
    obj1.property_values()

    value1 = int(input("Введите значение value1: "))
    value2 = int(input("Введите значение value2: "))
    obj2 = NewClass(value1, value2)
    obj2.property_values()

    del obj1
    del obj2

except ValueError:
    print("Ошибка: введите правильные данные.")













#2.3

#1

class Worker:
    def __init__(self, name, surname, bet, days):
        self.name = name
        self.surname = surname
        self.bet = bet
        self.days = days

    def GetSalary(self):
        salary = self.bet * self.days
        return salary

    def show_info(self):
        print(f"Работник: {self.name} {self.surname}")
        print(f"Ставка за день: {self.bet}")
        print(f"Количество отработанных дней: {self.days}")
        print(f"Зарплата: {self.GetSalary()}")


try:
    name = input("Введите имя работника: ")
    surname = input("Введите фамилию работника: ")
    bet = float(input("Введите ставку за день работы: "))
    days = int(input("Введите количество отработанных дней: "))

    worker = Worker(name, surname, bet, days)
    worker.show_info()

except ValueError:
    print("Ошибка: введите верные данные.")






#2
class Worker:
    def __init__(self, name, surname, bet, days):
        self.__name = name
        self.__surname = surname
        self.__bet = bet
        self.__days = days

    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname

    def get_bet(self):
        return self.__bet

    def get_days(self):
        return self.__days

    def get_salary(self):
        return self.__bet * self.__days

    def show_info(self):
        """Метод для вывода информации о работнике"""
        print(f"Работник: {self.get_name()} {self.get_surname()}")
        print(f"Ставка за день: {self.get_bet()}")
        print(f"Количество отработанных дней: {self.get_days()}")
        print(f"Зарплата: {self.get_salary()}")


try:
    name = input("Введите имя работника: ")
    surname = input("Введите фамилию работника: ")
    bet = float(input("Введите ставку за день работы: "))
    days = int(input("Введите количество отработанных дней: "))

    worker = Worker(name, surname, bet, days)
    worker.show_info()

except ValueError:
    print("Ошибка: введите верные данные.")








#3
class Calculation:
    def __init__(self, calculation_line=""):
        self.calculation_line = calculation_line

    def SetCalculationLine(self, new_line):
        self.calculation_line = new_line

    def SetLastSymbolCalculationLine(self, symbol):
        self.calculation_line += symbol

    def GetCalculationLine(self):
        return self.calculation_line

    def GetLastSymbol(self):
        if self.calculation_line:
            return self.calculation_line[-1]
        return None

    def DeleteLastSymbol(self):
        if self.calculation_line:
            self.calculation_line = self.calculation_line[:-1]


calc = Calculation()

while True:
    print("\nТекущая строка вычислений:", calc.GetCalculationLine())
    print("1. Изменить всю строку")
    print("2. Добавить символ в конец")
    print("3. Показать последний символ")
    print("4. Удалить последний символ")
    print("5. Выйти")

    choice = input("Выберите действие (1-5): ")

    if choice == "1":
        new_line = input("Введите новую строку вычислений: ")
        calc.SetCalculationLine(new_line)

    elif choice == "2":
        symbol = input("Введите символ для добавления: ")
        if len(symbol) == 1:
            calc.SetLastSymbolCalculationLine(symbol)
        else:
            print("Ошибка: Введите только один символ!")

    elif choice == "3":
        last_symbol = calc.GetLastSymbol()
        if last_symbol is not None:
            print("Последний символ:", last_symbol)
        else:
            print("Строка пуста.")

    elif choice == "4":
        calc.DeleteLastSymbol()
        print("Последний символ удалён.")

    elif choice == "5":
        print("Выход из программы.")
        break

    else:
        print("Ошибка: выберите число от 1 до 5.")


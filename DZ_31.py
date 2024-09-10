# Задание 1
# При старте приложения запускаются три потока. Первый поток заполняет список случайными числами.
# Два других потока ожидают заполнения. Когда список заполнен оба потока запускаются.
# Первый поток находит сумму элементов списка, второй поток среднеарифметическое значение в списке.
# Полученный список, сумма и среднеарифметическое выводятся на экран.
import threading
import random

class ListRandom():
    def __init__(self):
        self.rnd_numbers = []
        self.summa = 0
        self.average = 0

    def int_list(self):
        self.rnd_numbers = list(random.randint(0, 100) for i in range(10))
        print(self.rnd_numbers)

    def p_sum(self):
        self.summa = sum(self.rnd_numbers)
        print(self.summa)

    def p_avg(self):
        self.average = sum(self.rnd_numbers) / len(self.rnd_numbers)
        print(self.average)


f = ListRandom()

t1 = threading.Thread(target=f.int_list())
t2 = threading.Thread(target=f.p_sum())
t3 = threading.Thread(target=f.p_avg())

t1.start()
t1.join()

t2.start()
t3.start()

t2.join()
t3.join()

# Задание 2
# Пользователь с клавиатуры вводит путь к файлу. После чего запускаются три потока. Первый поток
# заполняет файл случайными числами. Два других потока ожидают заполнения. Когда файл заполнен
# оба потока стартуют. Первый поток находит все простые числа, второй поток факториал каждого числа
# в файле. Результаты поиска каждый поток должен записать в новый файл. На экран необходимо отобразить
# статистику выполненных операций.
import math


def generate_numbers(file_path):
    with open(file_path, 'w') as file:
        for _ in range(10):
            num = random.randint(1, 100)
            file.write(str(num) + '\n')


def find_prime_numbers(input_file, output_file):
    prime_numbers = []
    with open(input_file, 'r') as file:
        for line in file:
            num = int(line)
            if num > 1:
                is_prime = True
                for i in range(2, int(math.sqrt(num)) + 1):
                    if num % i == 0:
                        is_prime = False
                        break
            if is_prime:
                prime_numbers.append(num)

    with open(output_file, 'w') as file:
        for prime_num in prime_numbers:
            file.write(str(prime_num) + '\n')


def calculate_factorials(input_file, output_file):
    factorials = []
    with open(input_file, 'r') as file:
        for line in file:
            num = int(line)
            factorial = math.factorial(num)
            factorials.append(factorial)

    with open(output_file, 'w') as file:
        for factorial in factorials:
            file.write(str(factorial) + '\n')


if __name__ == '__main__':
    file_path = input('Введите путь к файлу: ')

    input_file = 'random.txt'
    output_prime_file = 'prime_numbers.txt'
    output_factorial_file = 'factorials.txt'

    t1 = threading.Thread(target=generate_numbers, args=(file_path,))
    t2 = threading.Thread(target=find_prime_numbers, args=(file_path, output_prime_file))
    t3 = threading.Thread(target=calculate_factorials, args=(file_path, output_factorial_file))

    t1.start()
    t1.join()

    t2.start()
    t3.start()

    t2.join()
    t3.join()

    print('Простые числа записаны в файл:')
    with open('prime_numbers.txt', 'r') as file:
        for line in file:
            print(int(line))

    print('Факториалы чисел записаны в файл:')
    with open('factorials.txt', 'r') as file:
        for line in file:
            print(int(line))

# Задание 3
# Пользователь с клавиатуры вводит путь к существующей директории и к новой директории. После чего
# запускается поток, который должен скопировать содержимое директории в новое место. Необходимо
# сохранить структуру директории. На экран необходимо отобразить статистику выполненных операций.
import os
import shutil


def copy_directory(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)

    for item in os.listdir(src):
        current_item = os.path.join(src, item)
        new_item = os.path.join(dst, item)

        if os.path.isdir(current_item):
            copy_directory(current_item, new_item)
        else:
            shutil.copy2(current_item, new_item)


current_directory = input("Введите путь к существующей директории: ").replace("\"", "")
new_directory = input("Введите путь к новой директории: ").replace("\"", "")

if not os.path.exists(current_directory):
    print(f"Директория {current_directory} не существует!")
else:
    thread = threading.Thread(target=copy_directory, args=[current_directory, new_directory])
    thread.start()
    thread.join()

# Задание 4
# Пользователь с клавиатуры вводит путь к существующей директории и слово для поиска. После чего
# запускаются два потока. Первый должен найти файлы, содержащие искомое слово и слить их содержимое
# в один файл. Второй поток ожидает завершения работы первого потока. После чего проводит вырезание
# всех запрещенных слов (список этих слов нужно считать из файла с запрещенными словами) из
# полученного файла. На экран необходимо отобразить статистику выполненных операций.


def find_files(directory, word, result_file):
    with open(result_file, 'w') as result:
        for root, _, files in os.walk(directory):
            for file in files:
                with open(os.path.join(root, file), 'r') as f:
                    if word in f.read():
                        result.write(f'{os.path.join(root, file)}\n')


def remove_ban_words(result_file, ban_words_file):
    with open(result_file, 'r') as result, open(ban_words_file, 'r') as ban:
        ban_words = set(word.strip() for word in ban)
        content = result.read()
        for word in ban_words:
            content = content.replace(word, '')
    with open(result_file, 'w') as result:
        result.write(content)


if __name__ == '__main__':
    directory = input("Введите путь к директории: ")
    word = input("Введите слово для поиска: ")

    result_file = 'result.txt'
    ban_words_file = 'ban_words.txt'

    t1 = threading.Thread(target=find_files, args=(directory, word, result_file))
    t2 = threading.Thread(target=remove_ban_words, args=(result_file, ban_words_file))

    t1.start()
    t1.join()

    t2.start()
    t2.join()
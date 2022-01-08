from tkinter import *
from tkinter import messagebox
from random import randint
import math
import numpy as np


def rand_number(n):  # генерация рандомного числа определённой длины
    range_start = pow(10, n-1)
    range_end = pow(10, n) - 1
    return randint(range_start, range_end)


def generate():
    txt_2.delete(0, END)
    txt_3.delete(0, END)
    txt_4.delete(0, END)
    txt_5.delete(0, END)
    txt_6.delete(0, END)
    txt_7.delete(0, END)
    # предупреждающие сообщения о заполненности всех полей
    if len(txt_1.get()) == 0:
        messagebox.showwarning('Внимание!', 'Введите размерность n!')
    else:
        size_n = int(txt_1.get())  # размерность n
        size_p = size_n // 2  # размерность p
        size_q = size_n - size_p  # размерность q

        len_p = int(math.log10(2 ** size_p)) + 1
        len_q = int(math.log10(2 ** size_q)) + 1

        p = rand_number(len_p)  # генерация случайного p
        q = rand_number(len_q)  # генерация случайного q

        while p % 2 == 0:
            p = rand_number(len_p)  # генерируем нечетный p
        while q % 2 == 0:
            q = rand_number(len_q)  # генерируем нечетный q

        while not miller_rabin_test(p):  # пока p составное
            p += 2  # добавляем 2, получаем опять нечётное число
            print(miller_rabin_test(p))

        while not miller_rabin_test(q):  # пока p составное
            q += 2  # добавляем 2, получаем опять нечётное число

        txt_2.insert(0, str(p))
        txt_3.insert(0, str(q))

        n = p * q  # вычисление n
        len_n = len(str(n))
        txt_4.insert(0, str(n))

        fi = (p - 1) * (q - 1)  # вычисление функции Эйлера
        txt_5.insert(0, str(fi))

        len_e = int(len_n/3)
        e = rand_number(len_e)

        nod = 0
        while nod != 1:  # e взаимнопростое с fi, т.е нод = 1
            e = rand_number(len_e)  # новое е
            nod, y0 = rae(e, fi)  # новый нод
            if e < 2 or e >= n:  # если е не прин-т полуинтервалу [2; n)
                e = rand_number(len_e)  # новое е
                nod, y0 = rae(e, fi)  # новый нод
        txt_6.insert(0, str(e))

        d = 0
        while 1 >= d or d >= n:  # d должен принадлежать интервалу (1, n)
            d = inverse_modulo(e, fi)  # d  это обратный элемент к e по модулю fi
        txt_7.insert(0, str(d))


def encrypt():
    txt_9.delete("0.0", 'end-1c')
    message = txt_8.get('0.0', 'end-1c')  # текст считали

    codes = []  # список кодов для каждого символа
    encrypt_codes = []  # список зашифрованных кодов

    for i in message:
        codes.append(ord(i))
    print(codes)

    e = int(txt_6.get())
    n = int(txt_4.get())

    for c in codes:
        h = fast_power(c, e, n)
        encrypt_codes.append(h)

    encrypt_codes.reverse()  # сохраняем порядок

    for t in encrypt_codes:
        txt_9.insert(0.0, '\n')
        txt_9.insert(0.0, t)


def decrypt():
    txt_10.delete("0.0", 'end-1c')
    cryptogram = txt_9.get('0.0', 'end-1c')
    cr_codes = []
    decrypt_message = ''

    d = int(txt_7.get())
    n = int(txt_4.get())

    cryptogram = cryptogram.split('\n')
    cryptogram.remove(cryptogram[len(cryptogram) - 1])
    for i in cryptogram:
        cr_codes.append(int(i))

    for h in cr_codes:
        c = fast_power(h, d, n)
        if c > 1114111:  # диапазон кодов в utf-8
            c = str(c)
            c = c[:5]
            c = int(c)
        decrypt_message += chr(c)

    txt_10.insert(0.0, decrypt_message)


def fast_power(number, degree, module):
    result = 1
    number %= module
    while degree:
        if degree & 1:
            result = (result * number) % module
        degree >>= 1
        number = (number * number) % module
    return result


def miller_rabin_test(number):  # является ли число простым (Алгоритм Миллера Рабина)

    rounds = int(math.log2(number))  # число раундов

    if number == 2 or number == 3:
        return True  # число простое
    if number < 2 or number % 2 == 0:
        return False
    # p - 1 = 2 ^ s * d, d - нечётное
    d = number - 1
    s = 0  # храним степень двойки

    while d % 2 == 0:
        d //= 2
        s += 1
    # когда мы получили остаток при делении, мы нашли нечетное d и степень двойки s
    # в каждом раунде выбираем случайное число из диапазона[2, number−1]
    # а - свидетель непростоты

    for i in range(rounds):
        a = randint(2, number)
        x = fast_power(a, d, number)

        if x == 1 or x == number - 1:
            continue

        for rounds in range(1, s):
            x = fast_power(x, 2, number)  # x ← x^2 mod n
            if x == 1:  # если x == 1, то вернуть "составное"
                return False
            if x == number - 1:  # если x == n − 1, то перейти на следующую итерацию внешнего цикла
                break
        if x != number - 1:
            return False
    return True


def rae(a, b):  # расширенный алгоритм евклида

    x0, x1, y0, y1 = 1, 0, 0, 1
    while b:
        q = a // b  # берём целую часть от деления
        a, b = b, a % b
        x0, x1 = x1, x0 - x1 * q
        y0, y1 = y1, y0 - y1 * q

    nod = a
    return nod, y0


def correct_module(number, module):  # число по модулю
    result = number % module
    if np.sign(result) * np.sign(module) < 0:
        result += module
    return result


def inverse_modulo(num, module):  # обратный элемент по модулю
    nod, inverse = rae(module, num)
    if nod != 1:
        return 0
    else:
        if inverse < 0:
            inverse = correct_module(inverse, module)
        return inverse


window = Tk()  # создали окно
window.title("RSA")  # заголовок окна
window.geometry("1100x400")

lbl_1 = Label(window, text='Размерность n:', font='Times 10')
lbl_1.grid(column=0, row=0, sticky=NW, padx=35, pady=5)  # вывод лэйбла
txt_1 = Entry(window, width=40)


txt_1.grid(column=0, row=1, padx=35, sticky=NW)
lbl_2 = Label(window, text='p:', font='Times 10')
lbl_2.grid(column=0, row=3, sticky=NW, padx=35)  # вывод лэйбла
txt_2 = Entry(window, width=40)
txt_2.grid(column=0, row=4, padx=35, sticky=NW)

lbl_3 = Label(window, text='q:', font='Times 10')
lbl_3.grid(column=0, row=5, sticky=NW, padx=35)  # вывод лэйбла
txt_3 = Entry(window, width=40)
txt_3.grid(column=0, row=6, padx=35, sticky=NW)

lbl_4 = Label(window, text='n:', font='Times 10')
lbl_4.grid(column=0, row=7, sticky=NW, padx=35)  # вывод лэйбла
txt_4 = Entry(window, width=40)
txt_4.grid(column=0, row=8, padx=35, sticky=NW)

lbl_5 = Label(window, text='φ(n):', font='Times 10')
lbl_5.grid(column=0, row=9, sticky=NW, padx=35)  # вывод лэйбла
txt_5 = Entry(window, width=40)
txt_5.grid(column=0, row=10, padx=35, sticky=NW)

lbl_6 = Label(window, text='e:', font='Times 10')
lbl_6.grid(column=0, row=11, sticky=NW, padx=35)  # вывод лэйбла
txt_6 = Entry(window, width=40)
txt_6.grid(column=0, row=12, padx=35, sticky=NW)

lbl_7 = Label(window, text='d:', font='Times 10')
lbl_7.grid(column=0, row=13, sticky=NW, padx=35)  # вывод лэйбла
txt_7 = Entry(window, width=40)
txt_7.grid(column=0, row=14, padx=35, sticky=NW)

btn_1 = Button(window, text="Сгенерировать", font='Times 10', width=30, command=generate)
btn_1.grid(column=1, row=0, pady=5)
txt_8 = Text(window, width=30, height=20)
txt_8.grid(column=1, row=1, rowspan=16)

btn_2 = Button(window, text="Зашифровать", font='Times 10', width=30, command=encrypt)
btn_2.grid(column=2, row=0, pady=5)
txt_9 = Text(window, width=30, height=20)
txt_9.grid(column=2, row=1, rowspan=16)

btn_3 = Button(window, text="Расшифровать", font='Times 10', width=30, command=decrypt)
btn_3.grid(column=3, row=0, pady=5)
txt_10 = Text(window, width=30, height=20)
txt_10.grid(column=3, row=1, rowspan=16)

window.mainloop()

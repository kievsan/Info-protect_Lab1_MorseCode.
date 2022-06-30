# This is a simple Python script.

# Защита информации (ЭКЗ)
#
# ЛАБОРАТОРНАЯ РАБОТА №1:
# ЗАДАНИЕ
# Реализовать возможность кодирования открытого текста
# и декодироваия шифрограммы по правилам азбуки Морзе.
# Предусмотреть поддержку русского и английского алфавита.

# Легко масштабируется под любое количество языков
# добавлением файлов кодовых таблиц и пунктов меню _menuMorse

from pprint import pprint
import Morse


def start_menu(section, taskMorse):
    menu = Morse._menuMorse[section]
    question = ''
    items = 0
    for item in menu:
        items += 1
        question += str(items) + ' - ' + item['name'] + ', '
    try:
        task = int(input(section + '? (' + question[0:-2] + ') >>'))
        if 1 <= task <= items:
            taskMorse[section] = menu[task - 1]
    except:
        pass  # Для тех, кто "в танке"...
    print('\t', taskMorse[section]['name'])
    return taskMorse


def is_exit(question):
    ex = input(question + ' ("y" - Ok) >>')
    return ex == 'y' or ex == 'Y' or ex == 'н' or ex == 'Н'


if __name__ == '__main__':
    while not is_exit('Хотите завершить?'):
        taskMorse = start_menu('language', Morse._startTaskMorse)
        taskMorse = start_menu('mode', taskMorse)
        msg = str(input('Enter data for ' +
                        taskMorse['mode']['name'] + '(' +
                        taskMorse['language']['name'] + ') >> '))
        if msg:
            taskMorse['incomingMessage'] = msg
        if taskMorse['mode']['name'].lower() == 'encode':
            task1 = Morse.Encoder(taskMorse)
        else:
            task1 = Morse.Decoder(taskMorse)
        print('\nЗапущен', task1)
        print(f'Получен результат >>\t{task1.translate()}')

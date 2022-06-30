#

from pprint import pprint

_menuMorse = {
    'language': [
        {'name': 'ENG', 'codeTable': 'morse_eng.txt'},
        {'name': 'RUS', 'codeTable': 'morse_rus.txt'}],
    'mode': [{'name': 'DECode'}, {'name': 'ENCode'}]}

_startTaskMorse = {'language': _menuMorse['language'][0],
                   'mode': _menuMorse['mode'][0],
                   'incomingMessage': '.... . .-.. .-.. --- --..-- .-- --- .-. .-.. -.. -.-.--'}  # hello,world!


def get_MorseCodeTable(language, file):
    print('\nDownloading Morse encode decode tables on ' + language + '...')
    codes_dict = {}
    try:
        with open(file, 'r', encoding='utf-8') as f:
            for line_of_matching in f:
                l = line_of_matching.strip()
                if not l:
                    continue
                symbol, morse_line = l.strip().split(' ')
                codes_dict[symbol.strip().lower()] = morse_line.strip()
    except FileNotFoundError as ex:
        print(f'File "{f}" not found...\n\t{ex}\n')
    except OSError as other:
        print(f'При открытии файла "{f}" возникли проблемы: \n\t{other}\n')
    print('Completed!')
    return codes_dict


def get_MorseCodeTables(refresh=False):
    if refresh:
        get_MorseCodeTables.codes_dict = {}
    if get_MorseCodeTables.codes_dict:
        return get_MorseCodeTables.codes_dict
    for language in _menuMorse['language']:
        get_MorseCodeTables.codes_dict[language['name']] = get_MorseCodeTable(
            language['name'], language['codeTable'])
    return get_MorseCodeTables.codes_dict


get_MorseCodeTables.codes_dict = {}


class _App:
    _func_name = 'аппликатор азбуки Морзе'

    def __init__(self, task, role=_func_name):
        self.role = role
        self.task = task
        self.incoming_list = self.task['incomingMessage'].lower().split(' ')
        self.code_tables = get_MorseCodeTables()[self.task['language']['name']]

    def __str__(self):
        return f'{self.get_purpose()}\n'

    def get_purpose(self):
        return self.role

    def _translate_path(self):
        return {'keys': list(self.code_tables.keys()),
                'values': list(self.code_tables.values()),
                'beingTranslated': ''.join([str(i) for i in self.incoming_list])}

    def _translated_complete(self, translated_message):
        return translated_message.strip()

    def translate(self):
        keys_list = self._translate_path()['keys']
        values_list = self._translate_path()['values']
        incoming_message = self._translate_path()['beingTranslated']
        print('\tИсходное сообщение:', incoming_message)
        translated_message = ''
        for one_char in incoming_message:
            try:
                index = keys_list.index(one_char)
                translated_char = values_list[index]
            except ValueError as ex:
                print(f'char "{one_char}" not found...\n\t{ex}\n')
                translated_char = '?'
            translated_message += translated_char + " "
        return self._translated_complete(translated_message)


class Encoder(_App):
    _func_name = 'кодировщик азбуки Морзе'

    def __init__(self, task):
        super(Encoder, self).__init__(task, self._func_name)


class Decoder(_App):
    _func_name = 'декодер азбуки Морзе'

    def __init__(self, task):
        super(Decoder, self).__init__(task, self._func_name)

    def _translate_path(self):
        return {'keys': list(self.code_tables.values()),
                'values': list(self.code_tables.keys()),
                'beingTranslated': self.incoming_list}

    def _translated_complete(self, translated_message):
        return ''.join([str(i) for i in translated_message.strip().split(' ')])

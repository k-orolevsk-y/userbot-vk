import config

types = {
    'user': ['error', "Необходимо ответить на сообщение пользователя или указать на него ссылку: {}"],
    'correct_use': ['invalid', "Правильное использование: {}"]
}


def getMessage(type_error, text='Ошибка!', custom_error=()):
    out = ''
    if type_error != 'custom':
        situation = types[type_error]
        out += f"{config.prefixes[situation[0]]} "
        out += situation[1].format(text)
    else:
        out += f"{config.prefixes[custom_error[0]]} "
        out += custom_error[1]
    return out

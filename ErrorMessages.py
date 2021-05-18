import config

def getMessage(command):
    out = f"{config.prefixes['error']} Необходимо ответить на сообщение пользователя или указать на него ссылку: {command} [пользователь]"
    return out
class UserBotExceptions(Exception):
    pass

class CustomError(UserBotExceptions):
    def __init__(self, text):
        self.txt = text
    def __str__(self):
        return(self.txt)

class skipHandle(UserBotExceptions):
    def __init__(self):
        self.txt = f"&#9889; Дальше обработку сообщения нет смысла проводить"
    def __str__(self):
        return(self.txt)
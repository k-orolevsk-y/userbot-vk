"""
    Автоматическая установка модулей необходимых для работы бота.
"""

import os
from importlib.util import *

modules = {
    "vk_api": "vk_api",
    "ujson": "ujson",
    "PIL": "pillow",
    "requests": "requests",
    "termcolor": "termcolor",
}
for module in modules:
    if find_spec(module) is None:
        print(f"\033[31mУстановка модуля {modules[module]}\033[37m")
        os.system(f"pip3.10 install {modules[module]}")

os.system('clear')
print(f"\033[32mТерминал очищен, модули установлены!")

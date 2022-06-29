# Юзербот для [vk.com](https://vk.com/)

## ПОЛНАЯ РАБОТОСПОСОБНОСТЬ ГАРАНТИРУЕТСЯ ТОЛЬКО НА Linux!

### Запуск на Linux: 

```        
sh start.sh
```

___

### Необходимые зависимости Python3.10: 

- ujson
- requests
- pillow
- vk_api
- termcolor

***Данные модули можно установить отдельно.***\
***Для этого необходимо запустить***
```
python3.10 install_modules.py
```

---

### Необходимые программы для работы некоторых команд:

- imagemagick
- ffmpeg

***Данные модули можно установить отдельно.***\
***Для этого необходимо запустить***

```
sudo apt install imagemagick ffmpeg -y
```

### Необходимые настройки можете установить в ```config.py```

```
nano config.py
```

### Команды:

___/911, /112, /help - информация по командам,___

___/del - [количество] [необходимо ли убрать содержимое] - удалить сообщения,___

___/disable - отключаем бота для общедоступного использования,___

___/copy - скопировать чужое аудиосообщение,___

___/i, /и [время (необязательно)] [текст] - отправить исчезайку (есть баги),___

___/repeat [количество] [текст] - повторит сообщение с определенным интервалом,___

___/ban [пользователь] - заблокировать пользователя (бот не будет реагировать на юзера),___

___/ban_chat - заблокировать беседу (бот не будет работать в беседе),___

___/assoc - список ассоциаций,___

___/assoc_set - добавить ассоциацию,___

___/assoc_del - удалить ассоциацию,___

___/unban [пользователь] - разблокировать пользователя,___

___/unban_chat - разблокировать беседу,___

___/ignore [пользователь] - кинуть пользователя в игнор,___

___/unignore [пользователь] - удалить пользователя из игнора,___

___/uid, /userid - получить ID пользователя,___

___/tc [пользователь] - проверка на тестера,___

___/stickers [пользователь] - выводит стикеры пользователя,___

___/d, /dist - жмых картинок,___ ***`*`***

___/au, /audio - жмых голосового,___ ***`*`***

___/sa, /save_audio - сохранить голосовое сообщение,___

___/ag, /aget - отправить сохранённое голосовое сообщение,___

___/ad, /adelete - удалить сохранённое голосовое сообщение,___

___/alist - список сохранённых голосовых сообщений,___

___/ma, /music_audio - перевести песню в голосовое,___ ***`*`***

___/n, /negative - перевести фотографию в негатив,___ ***`*`***

___/t, /text -- добавить текст к фотографии,___ ***`*`***

___+s, +saves, +с, +сохры - открыть сохры пользователю,___

___-s, –saves, -с, -сохры - закрыть сохры пользователю,___

___+a, +audios, +м, +музыка - открыть аудиозаписи пользователю,___

___-a, -audios, -м, -музыка - закрыть аудиозаписи пользователю___

___

***`*`*** - *команды могут выполняться от 1 до 15 секунд, зависит от сервера на котором стоит бот.*
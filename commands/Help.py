commands = {
    "public": [
        {
            "commands_alias": ["/au", "/audio"],
            "description": "жмых голсового сообщения",
        },
        {
            "commands_alias": ["/d", "/dist"],
            "description": "жмых фотографии",
        },
        {
            "commands_alias": ["/ma", "/music_audio"],
            "description": "первести песню в голосовое сообщение",
        },
        {
            "commands_alias": ["/n", "/negative"],
            "description": "первести фотогарфию в негатив",
        },
        {
            "commands_alias": ["/t", "/text"],
            "description": "добавить текст к фотографии",
        },
        {
            "commands_alias": ["/tc", "/tester_check"],
            "description": "проверить пользователя на тестера",
        },
        {
            "commands_alias": ["/st", "/stickers"],
            "description": "узнать количество стикеров пользователя и цену",
        },
        {
            "commands_alias": ["/userid", "/uid"],
            "description": "получить ID пользователя",
        },
    ],
    "private": [
        {
            "commands_alias": ["/ban"],
            "description": "заблокировать доступ к боту пользователю",
        },
        {
            "commands_alias": ["/ban_chat"],
            "description": "заблокировать чат (бот не будет в нем работать)",
        },
        {
            "commands_alias": ["/assoc"],
            "description": "список ассоциаций",
        },
        {
            "commands_alias": ["/assoc_set"],
            "description": "добавить ассоциацию",
        },
        {
            "commands_alias": ["/assoc_del"],
            "description": "удалить ассоциацию",
        },
        {
            "commands_alias": ["/ignore"],
            "description": "добавить пользователя в игнор (его сообщения будут удалятся для вас)",
        },
        {
            "commands_alias": ["/copy"],
            "description": "скопировать голосовое сообщение",
        },
        {
            "commands_alias": ["/del"],
            "description": "удалить сообщения",
        },
        {
            "commands_alias": ["/disable"],
            "description": "отключить бота для общедоступного использования",
        },
        {
            "commands_alias": ["/i", "/и"],
            "description": "отправить исчезающее сообщение",
        },
        {
            "commands_alias": ["/repeat"],
            "description": "спам сообщениями",
        },
        {
            "commands_alias": ["/sa", "/save_audio"],
            "description": "сохранить голосовое сообщение",
        },
        {
            "commands_alias": ["/ag", "/aget"],
            "description": "отправить сохранённое голосовое сообщение",
        },
        {
            "commands_alias": ["/ad", "/adelete"],
            "description": "удалить сохранённое голосовое сообщение",
        },
        {
            "commands_alias": ["/alist"],
            "description": "список сохранённых голосовых сообщений",
        },
        {
            "commands_alias": ["/unban"],
            "description": "разблокировать пользователя",
        },
        {
            "commands_alias": ["/unban_chat"],
            "description": "разблокировать чат",
        },
        {
            "commands_alias": ["/unignore"],
            "description": "удалить из игнора пользователя",
        },
    ]
}


def get_commands(type_commands):
    out = ""
    for command in commands[type_commands]:
        alias_transform = ", ".join(command['commands_alias'])
        description = command['description']
        out += f"{alias_transform} -- {description}\n"
    return out


def cmd(api, message, owner_id):
    universal_message = "\n🐺 Разработчики: [id171812976|тык], [id163653953|тык] [id413636725|тык]"
    github = "\n❔ Полный список команд и обновления можно посмотреть тут: https://korolevsky.me?ub"
    main_message = f"🚑 Доступные команды >>\n{get_commands('public')}"

    if message['from_id'] == owner_id:
        main_message += f"\n❗️ Команды владельца:\n{get_commands('private')}"
        universal_message += github

    main_message += universal_message

    api.messages.send(
        peer_id=message['peer_id'],
        random_id=0,
        message=main_message,
        reply_to=message['id']
    )

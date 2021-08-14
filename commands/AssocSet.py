import config
import functions
from commands import Help

def cmd(vk, message, args):
    peer_id = message['peer_id']
    for_all = None if message['from_id'] == message['peer_id'] else True

    if len(args) < 3:
        functions.msg_edit(
            vk, peer_id, message['id'],
            f"{config.prefixes['invalid']} Правильное использование: /assoc_set [команда] [ассоциация]",
            for_all=for_all
        )
        return

    key = args[1].lower()
    assoc = args[2].lower()

    flag = False
    for i in Help.commands.keys():  # Не бейте за рекурсии, иначе ночью (03:14) не придумал
        commands_info = Help.commands[i]
        for j in range(len(commands_info)):
            commands = commands_info[j]['commands_alias']
            for n in range(len(commands)):
                if commands[n].lower() == key:
                    flag = True

    if not flag:
        functions.msg_edit(
            vk, peer_id, message['id'],
            f"{config.prefixes['error']} Такой команды нет, учтите, что необходимо писать команду полностью.\n👉🏻 Например: /ban",
            for_all=for_all
        )
        return

    data = functions.getData('assoc')
    if data is None:
        data = {}

    for k in data.keys():
        if k == assoc:
            functions.msg_edit(
                vk, peer_id, message['id'],
                f"{config.prefixes['error']} Ассоциация `{assoc}` уже существует!",
                for_all=for_all
            )
            return

    data[assoc] = key
    functions.editData('assoc', data)

    functions.msg_edit(
        vk, peer_id, message['id'],
        f"{config.prefixes['success']} Создана новая ассоциаця для команды {key}: `{assoc}`!",
        for_all=for_all,
        sleeping=5
    )
    return

import config
import functions

def cmd(vk, message, args):
    peer_id = message['peer_id']
    for_all = None if message['from_id'] == message['peer_id'] else True

    assocs = functions.getData('assoc')
    if assocs is None:
        assocs = {}

    if len(args) < 2:
        functions.msg_edit(
            vk, peer_id, message['id'],
            f"{config.prefixes['invalid']} Правильное использование: /assoc_del [ассоциация]",
            for_all=for_all
        )
        return

    key = str(message['text'].split(' ', 1)[1])
    if assocs.get(key) is None:
        functions.msg_edit(
            vk, peer_id, message['id'],
            f"{config.prefixes['invalid']} Ассоциации с таким ключем нет!",
            for_all=for_all
        )
        return

    assocs.pop(key)
    functions.editData('assoc', assocs)

    functions.msg_edit(vk, peer_id, message['id'], f"{config.prefixes['success']} Ассоциация `{key}` была успешно удалена.", for_all=for_all)
    return

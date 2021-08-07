import config
import functions

def cmd(vk, message, args):
    peer_id = message['peer_id']
    for_all = None if message['from_id'] == message['peer_id'] else True

    audios = functions.getData('saved_audio')
    if audios is None:
        audios = {}

    if len(args) < 2:
        functions.msg_edit(
            vk, peer_id, message['id'],
            f"{config.prefixes['invalid']} Правильное использование: /adelete [ключ]",
            for_all=for_all
        )
        return

    key = str(message['text'].split(' ', 1)[1])
    if audios.get(key) is None:
        functions.msg_edit(
            vk, peer_id, message['id'],
            f"{config.prefixes['invalid']} Голсового сообщения с таким ключем нет!",
            for_all=for_all
        )
        return

    audios.pop(key)
    functions.editData('saved_audio', audios)

    functions.msg_edit(vk, peer_id, message['id'], f"{config.prefixes['success']} Голосовое сообщение `{key}` было успешно удалено.", for_all=for_all)
    return

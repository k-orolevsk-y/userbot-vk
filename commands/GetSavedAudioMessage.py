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
            f"{config.prefixes['invalid']} Правильное использование: /ag [ключ]",
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

    reply = None
    if message.get('reply_message') is not None:
        reply = message['reply_message']['id']

    functions.msg_edit(vk, peer_id, message['id'], "&#13;", for_all=for_all, sleeping=0)
    functions.msg_send(vk, peer_id, attachment=audios.get(key), reply_to=reply)
    return

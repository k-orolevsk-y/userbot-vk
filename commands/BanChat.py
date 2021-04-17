import time
import config
import functions


def cmd(api, message, args):
    for_all = None if message['from_id'] == message['peer_id'] else True

    banned = functions.getData('banned_peers')
    if banned is None: banned = []

    if message['peer_id'] in banned:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['invalid']} Данная беседа уже заблокирована."
        )
        time.sleep(3)
        api.messages.delete(
            message_ids=message['id'],
            delete_for_all=for_all
        )

    banned.append(message['peer_id'])
    edit = functions.editData('banned_peers', banned)

    if edit:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['success']} Данная беседа была заблокирована!"
        )
    else:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['error']} Данную беседу не получилось заблокировать. Возможно данные повреждены."
        )

    return
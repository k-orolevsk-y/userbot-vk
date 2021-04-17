import config
import functions


def cmd(api, message):
    banned = functions.getData('banned_peers')
    if banned is None: banned = []

    if not (message['peer_id'] in banned):
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['invalid']} Данная беседа не заблокирована."
        )
        return

    banned.remove(message['peer_id'])
    edit = functions.editData('banned_peers', banned)

    if edit:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['success']} Данная беседа была разблокирована!"
        )
    else:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['error']} Данную беседу не получилось разблокировать. Возможно данные повреждены."
        )

    return

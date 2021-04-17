import time
import config
import functions


def cmd(api, message, args, owner_id):
    for_all = None if message['from_id'] == message['peer_id'] else True

    if message.get('reply_message') is not None:
        target = api.users.get(
            user_ids=message['reply_message']['from_id']
        )
    else:
        try:
            target = api.users.get(
                user_ids=functions.getUserId(args[1])
            )
        except:
            api.messages.edit(
                peer_id=message['peer_id'],
                message_id=message['id'],
                message=f"{config.prefixes['error']} Необходимо ответить на сообщение пользователя или указать на него ссылку: /ban [пользователь]"
            )
            time.sleep(3)
            api.messages.delete(
                message_ids=message['id'],
                delete_for_all=for_all
            )
            return

    banned = functions.getData('banned')
    if banned is None: banned = []

    target = target[0]
    if target['id'] in banned:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['invalid']} [id{target['id']}|{target['first_name']} {target['last_name']}] уже заблокирован."
        )
        return

    if owner_id == target['id']:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['invalid']} Нельзя заблокировать самого себя!"
        )
        return

    banned.append(target['id'])
    edit = functions.editData('banned', banned)

    if edit:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['success']} [id{target['id']}|{target['first_name']} {target['last_name']}] был заблокирован!"
        )
    else:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['error']} Пользователя [id{target['id']}|{target['first_name']} {target['last_name']}] не получилось заблокировать. Возможно данные повреждены."
        )

    return

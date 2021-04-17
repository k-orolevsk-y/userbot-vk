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
                message=f"{config.prefixes['error']} Необходимо ответить на сообщение пользователя или указать на него ссылку: /ignore [пользователь]"
            )
            time.sleep(3)
            api.messages.delete(
                message_ids=message['id'],
                delete_for_all=for_all
            )
            return

    ignored_users = functions.getData('ignore')
    if ignored_users is None: ignored_users = []

    target = target[0]
    if target['id'] in ignored_users:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['invalid']} [id{target['id']}|{target['first_name']} {target['last_name']}] уже игнорируется."
        )
        return

    if owner_id == target['id']:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message="❌ Нельзя игнорировать самого себя!"
        )
        return

    ignored_users.append(target['id'])
    edit = functions.editData('ignore', ignored_users)

    if edit:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['success']} [id{target['id']}|{target['first_name']} {target['last_name']}] теперь будет игнорироваться!"
        )
    else:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"Пользователя {config.prefixes['error']} [id{target['id']}|{target['first_name']} {target['last_name']}] не получилось отправить в игнор. Возможно данные повреждены."
        )

    return

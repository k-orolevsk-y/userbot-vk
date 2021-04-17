import time
import config
import functions


def cmd(api, message, args):
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
                message=f"{config.prefixes['error']} Необходимо ответить на сообщение пользователя или указать на него ссылку: /unignore [пользователь]"
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
    if not(target['id'] in ignored_users):
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['invalid']} [id{target['id']}|{target['first_name']} {target['last_name']}] не игнорируется."
        )
        return

    ignored_users.remove(target['id'])
    edit = functions.editData('ignore', ignored_users)

    if edit:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['success']} [id{target['id']}|{target['first_name']} {target['last_name']}] был удалён из списка игнорируемых!"
        )
    else:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"Пользователя {config.prefixes['error']} [id{target['id']}|{target['first_name']} {target['last_name']}] не получилось удалить из списка игнорируемых. Возможно данные повреждены."
        )

    return

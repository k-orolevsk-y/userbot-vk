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
                message=f"{config.prefixes['error']} Необходимо ответить на сообщение пользователя или указать на него ссылку: /uid [пользователь]"
            )
            time.sleep(3)
            api.messages.delete(
                message_ids=message['id'],
                delete_for_all=for_all
            )
            return

    api.messages.edit(
        peer_id=message['peer_id'],
        message_id=message['id'],
        message=f"{config.prefixes['success']} ID пользователя: {target[0]['id']}"
    )
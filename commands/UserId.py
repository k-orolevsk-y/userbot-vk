import time
import config
import functions


def cmd(api, message, owner_id, args):
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
            if owner_id == message['from_id']:
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
            else:
                api.messages.send(
                    peer_id=message['peer_id'],
                    reply_to=message['id'],
                    random_id=0,
                    message=f"{config.prefixes['error']} Необходимо ответить на сообщение пользователя или указать на него ссылку: /uid [пользователь]"
                )
            return

    if owner_id == message['from_id']:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['success']} ID пользователя: {target[0]['id']}"
        )
    else:
        api.messages.send(
            peer_id=message['peer_id'],
            reply_to=message['id'],
            random_id=0,
            message=f"{config.prefixes['success']} ID пользователя: {target[0]['id']}"
        )

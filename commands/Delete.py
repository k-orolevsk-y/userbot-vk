import time
import config
import random


def cmd(api, message, args, owner_id):
    for_all = None if message['from_id'] == message['peer_id'] else True

    if len(args) < 2:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['invalid']} Необходимо ввести количество сообщений от 1 до 20."
        )
        return

    api.messages.delete(message_ids=message['id'], delete_for_all=for_all)
    messages = api.messages.get_history(
        count=200,
        peer_id=message['peer_id'],
        start_message_id=message['id']
    )

    deleted = 0
    _sum = int(args[1])
    list_messages = []

    for msg in messages['items']:
        if deleted >= _sum:
            break

        times = int(time.time()) - msg['date']
        if times > 86400:
            break

        if msg['from_id'] == owner_id:
            try:
                if len(args) >= 3:
                    api.messages.edit(
                        peer_id=msg['peer_id'],
                        message_id=msg['id'],
                        message="&#13;"
                    )

                    time.sleep(random.uniform(0.25, 0.75))
            except Exception as e:
                print(e)

            list_messages.append(msg['id'])
            deleted += 1

    api.messages.delete(message_ids=list_messages, delete_for_all=for_all)
    return

import time
import config
import random


def cmd(api, message, args):
    for_all = None if message['from_id'] == message['peer_id'] else True

    if len(args) < 3:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['error']} Использование: /repeat [количество] [сообщение]"
        )
        time.sleep(1)
        api.messages.delete(
            message_ids=message['id'],
            delete_for_all=for_all
        )
        return

    try:
        sum_repeat = int(args[1])
        if sum_repeat < 0 or sum_repeat > 20:
            api.messages.edit(
                peer_id=message['peer_id'],
                message_id=message['id'],
                message=f"{config.prefixes['error']} Использование: /repeat [количество 1-20] [сообщение]"
            )
            time.sleep(1)
            api.messages.delete(
                message_ids=message['id'],
                delete_for_all=for_all
            )
            return
    except:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['error']} Использование: /repeat [количество 1-20] [сообщение]"
        )
        time.sleep(1)
        api.messages.delete(
            message_ids=message['id'],
            delete_for_all=for_all
        )
        return

    api.messages.delete(
        message_ids=message['id'],
        delete_for_all=for_all
    )

    text = message['text'].split(' ', 2)[2]
    for x in range(sum_repeat):
        try:
            api.messages.send(
                peer_id=message['peer_id'],
                random_id=0,
                message=text
            )
        except:
            break

        time.sleep(random.uniform(0, 2.5))
    return
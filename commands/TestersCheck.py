import config
import functions


def cmd(api, message, args, owner_id):
    if message.get('reply_message') is not None:
        user_id = message['reply_message']['from_id']
    else:
        user_id = functions.getUserId(args[1])

    try:
        target = api.users.get(user_ids=user_id)
        target = target.pop()
    except:
        api.messages.send(
            random_id=0,
            peer_id=message['peer_id'],
            message=f"{config.prefixes['error']} Необходимо ответить на сообщение пользователя или указать на него ссылку: /tc [пользователь]",
            reply_to=message['id']
        )
        return

    try:
        tester_bool = api.groups.is_member(group_id=134304772, user_id=target['id'])
    except:
        api.messages.send(
            random_id=0,
            peer_id=message['peer_id'],
            message=f"{config.prefixes['error']} Ограничение на проверку со стороны ВКонтакте.",
            reply_to=message['id']
        )
        return

    if not tester_bool:
        api.messages.send(
            peer_id=message['peer_id'],
            random_id=0,
            message=f"{config.prefixes['success_no']} [id{target['id']}|{target['first_name']} {target['last_name']}] не тестировщик из [testpool|/testpool].",
            reply_to=message['id'],
            disable_mentions=True
        )
    else:
        api.messages.send(
            peer_id=message['peer_id'],
            random_id=0,
            message=f"{config.prefixes['success']} [id{target['id']}|{target['first_name']} {target['last_name']}] тестировщик из [testpool|/testpool].\n\nhttps://vk.com/bugs?act=reporter&id={target['id']}",
            reply_to=message['id'],
            disable_mentions=True
        )

    return

import ujson
import config
import requests
import functions


def cmd(api, message, args, owner_id):
    try:
        if message.get('reply_message') is not None:
            user_id = message['reply_message']['from_id']
        else:
            user_id = functions.getUserId(args[1])

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

    tester_info = ujson.decode(requests.get(f"https://ssapi.ru/vk-bugs-api/?method=getReporter&reporter_id={target['id']}").text)
    if tester_info.get('error') is True:
        api.messages.send(
                peer_id=message['peer_id'],
                random_id=0,
                message=f"{config.prefixes['error']} Ошибка при обращении к API: {tester_info.get('error_msg')}",
                reply_to=message['id'],
                disable_mentions=True
        )
    else:
        tester_info = tester_info.get('response').get('reporter')
        if not tester_info.get('tester'):
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
                message=f"{config.prefixes['success']} [id{target['id']}|{target['first_name']} {target['last_name']}] тестировщик из [testpool|/testpool].\n\n• {tester_info.get('status_text')}\n• Количество отчётов: {tester_info.get('reports_count')}\n• Место в топе: {tester_info.get('top_position')}\n\nhttps://vk.com/bugs?act=reporter&id={target['id']}",
                reply_to=message['id'],
                disable_mentions=True
            )

    return

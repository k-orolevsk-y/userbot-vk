import ujson
import config
import requests
import functions


def cmd(api, message, args):
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
            message=f"{config.prefixes['error']} Необходимо ответить на сообщение пользователя или указать на него ссылку: /stickers [пользователь]",
            reply_to=message['id']
        )
        return

    stickers_info = ujson.decode(requests.get(f"https://ssapi.ru/vk-stickers-api/?method=getStickers&user_id={target['id']}").text)
    if stickers_info.get('error') is True:
        api.messages.send(
                peer_id=message['peer_id'],
                random_id=0,
                message=f"{config.prefixes['error']} Ошибка при обращении к API: {stickers_info.get('error_msg')}",
                reply_to=message['id'],
                disable_mentions=True
        )
    else:
        stickers_info = stickers_info.get('response')
        print(stickers_info)
        if stickers_info.get('info').get('paid') == 0:
            api.messages.send(
                peer_id=message['peer_id'],
                random_id=0,
                message=f"{config.prefixes['success']} [id{target['id']}|{target['first_name']} {target['last_name']}] имеет {functions.pluralForm(stickers_info.get('count'), ['стикерпак', 'стикерпака', 'стикерпаков'])}.\n🥺 Платных стикерпаков у пользователя нет.",
                reply_to=message['id'],
                disable_mentions=True
            )
        else:
            api.messages.send(
                peer_id=message['peer_id'],
                random_id=0,
                message=f"{config.prefixes['success']} [id{target['id']}|{target['first_name']} {target['last_name']}] имеет {functions.pluralForm(stickers_info.get('count'), ['стикерпак', 'стикерпака', 'стикерпаков'])} из них {functions.pluralForm(stickers_info.get('info').get('paid'), ['стикерпак платный', 'стикерпака платные', 'стикерпаков платные'])}.\n\n⚙️ Цена стикеров (в голосах / в рублях): {stickers_info.get('info').get('price_vote')} / {stickers_info.get('info').get('price')}₽",
                reply_to=message['id'],
                disable_mentions=True
            )

    return

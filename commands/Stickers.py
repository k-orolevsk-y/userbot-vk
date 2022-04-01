import json
import random
import time

import config
import requests
import functions


def get_token(api, message):
    resp = functions.getData('odeanon_token')
    if resp is not None:
        return resp
    else:
        config.odeanon_token = True
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['process']} Идёт получение токена"
        )
        api.messages.send(
            peer_id='-197641192',
            random_id=0,
            message='/api reset'
        )
        while True:
            time.sleep(1)
            print("While in progress")
            if functions.getData('odeanon_token') is None:
                continue
            else:
                config.odeanon_token = False
                return functions.getData('odeanon_token')


def get_random(list):
    count = len(list)
    resp = ''

    if count >= 3:
        for i in range(3):
            r = random.randint(0, count - 1)
            resp += f"{list.pop(r)['title']}, "

    else:
        for i in list:
            resp += f"{i['title']}"

    return resp


def get_styles(items):
    styles = []
    for i in items:
        for k in items[i]:
            if k.get('style') != 0:
                styles.append(k)

    return get_random(styles)


def cmd(api, message, args):
    reply = message.get('reply_message')
    tkn = get_token(api, message)
    progress = True

    if reply is not None:
        user_id = message['reply_message']['from_id']

    else:
        if len(args) < 2:
            api.messages.edit(
                peer_id=message['peer_id'],
                message_id=message['id'],
                message=f"{config.prefixes['error']} Правильное использование: /stickers [пользователь]"
            )
            progress = False
        else:
            user_id = functions.getUserId(args[1])

    if progress:
        target = api.users.get(
            user_ids=user_id
        )[0]

        stickers_info = json.loads(
            requests.get(
                f"https://api.korolevsky.me/method/stickers.get?access_token={tkn}&user_id={target['id']}").text
        )

        if 'error' in stickers_info:
            api.messages.edit(
                peer_id=message['peer_id'],
                message_id=message['id'],
                message=f"{config.prefixes['error']} Ошибка при обращении к API: {stickers_info['error_msg']}"
            )

        stickers_info = stickers_info['response']
        out_message = f"{config.prefixes['success']} [id{target['id']}|{target['first_name']} {target['last_name']}] имеет {functions.pluralForm(stickers_info['info']['count']['all'], ['стикерпак', 'стикерпака', 'стикерпаков'])}"
        paid_stickers = stickers_info['info']['count']['paid']

        if paid_stickers == 0:
            out_message += ".\n🥺 Платных стикерпаков у пользователя нет."

        else:
            info = stickers_info['info']
            items = stickers_info['items']
            price_votes = info['price_vote']
            price_rubles = info['price']
            out_message += f"\n\n🤕 Бесплатных стикеров: {info['count']['free']}\n\t{get_random(items['free'])}"
            out_message += f"\n\n🤑 Платных стикеров: {info['count']['paid']}\n\t{get_random(items['paid'])}"
            out_message += f"\n\n🎭 Стилей: {info['count']['styles']}\n\t{get_styles(items)}"
            out_message += f"\n\n😻 Цена стикеров: {functions.pluralForm(price_votes, ['голос', 'голоса', 'голосов'])} / {price_rubles}₽"

        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=out_message
        )

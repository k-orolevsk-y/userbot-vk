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
        try:
            api.messages.edit(
                peer_id=message['peer_id'],
                message_id=message['id'],
                message=f"{config.prefixes['process']} Идёт получение токена"
            )
        except:
            pass
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
    titles = []

    for i in list:
        titles.append(i['title'])

    if len(titles) >= 3:
        resp = f"{titles.pop(random.randint(0, len(titles) - 1))}, " \
                f"{titles.pop(random.randint(0, len(titles) - 1))}, " \
                f"{titles.pop(random.randint(0, len(titles) - 1))}"

    else:
        resp = ", ".join(titles)

    return resp


def get_from_type(items, _type):
    out = []

    for i in items:
        for k in items[i]:
            if k.get(_type) != 0:
                out.append(k)

    return get_random(out)


def cmd(api, message, args, owner_id):
    reply = message.get('reply_message')
    tkn = get_token(api, message)
    progress = True

    if reply is not None:
        user_id = message['reply_message']['from_id']

    else:
        if len(args) < 2:
            if message['from_id'] == owner_id:
                api.messages.edit(
                    peer_id=message['peer_id'],
                    message_id=message['id'],
                    message=f"{config.prefixes['error']} Правильное использование: /stickers [пользователь]"
                )
            else:
                api.messages.send(
                    peer_id=message['peer_id'],
                    random_id=0,
                    message=f"{config.prefixes['error']} Правильное использование: /stickers [пользователь]"
                )
            progress = False
        else:
            user_id = functions.getUserId(args[1])

    if progress:
        target = api.users.get(
            user_ids=user_id
        )[0]

        stickers_info = requests.get(
            f"https://api.korolevsky.me/method/stickers.get?access_token={tkn}&user_id={target['id']}"
        ).json()

        out_message = ''

        if not stickers_info['ok']:
            if stickers_info['error']['error_code'] == 429:
                out_message += f"{config.prefixes['error']} " \
                               f"Дневной лимит на стикеры достигнут либо слишком частое использование. \n" \
                               f"Для увеличения лимитов, оформите подписку VK Donut на @odeanon\n"

                if message['from_id'] == owner_id:
                    api.messages.edit(
                        peer_id=message['peer_id'],
                        message_id=message['id'],
                        message=out_message,
                        attachment="donut_link-197641192"
                    )
                else:
                    api.messages.send(
                        peer_id=message['peer_id'],
                        random_id=0,
                        message=out_message,
                        attachment="donut_link-197641192"
                    )

            else:
                out_message += f"{config.prefixes['error']} Произошла непредвиденная ошибка:\n" \
                               f"Description: {stickers_info['error'].get('error_msg')}\n" \
                               f"Error code: {stickers_info['error'].get('error_code')}\n\n" \
                               f"При возникновении ошибки пишите [id163653953|тык]"
                if message['from_id'] == owner_id:
                    api.messages.edit(
                        peer_id=message['peer_id'],
                        message_id=message['id'],
                        message=out_message,
                        disable_mentions=True
                    )
                else:
                    api.messages.send(
                        peer_id=message['peer_id'],
                        random_id=0,
                        message=out_message,
                        disable_mentions=True
                    )

        elif stickers_info['ok']:
            stickers_info = stickers_info['response']

            if f"{stickers_info}" == "[]":
                out_message += f"{config.prefixes['success_no']} " \
                               f"[id{target['id']}|{target['first_name']} {target['last_name']}] " \
                               f"был скрыт от просмотра в данном боте."
                if message['from_id'] == owner_id:
                    api.messages.edit(
                        peer_id=message['peer_id'],
                        message_id=message['id'],
                        message=out_message,
                        disable_mentions=True
                    )
                else:
                    api.messages.send(
                        peer_id=message['peer_id'],
                        random_id=0,
                        message=out_message,
                        disable_mentions=True
                    )

            else:
                info = stickers_info['info']
                items = stickers_info['items']
                price_votes = info['price_vote']
                price_rubles = info['price']

                out_message += f"[id{message['from_id']}|😻] [id{target['id']}|{target['first_name']} {target['last_name']}] " \
                               f"имеет {functions.pluralForm(stickers_info['info']['count']['all'], ['стикерпак', 'стикерпака', 'стикерпаков'])} " \
                               f"(из них {info['count']['paid']} платных, " \
                               f"{info['count']['styles']} стилей и " \
                               f"{info['count']['promo']} уникальных)\n"

                out_message += f"\n🐔 Из бесплатных: {get_random(items['free'])}"

                if info['count']['paid'] == 0:
                    out_message += ".\n🥺 Платных стикерпаков у пользователя нет"

                else:
                    out_message += f"\n🤑 Из платных: {get_random(items['paid'])}"

                if info['count']['styles'] > 0:
                    out_message += f"\n🎭 Из стилей: {get_from_type(items, 'styles')}"

                if info['count']['promo'] > 0:
                    out_message += f"\n🐹 Из уникальных: {get_from_type(items, 'promo')}"

                if price_votes > 0:
                    out_message += f"\n\n⚙ Общая сумма купленных и подаренных стикеров: {price_rubles}₽ ({functions.pluralForm(price_votes, ['голос', 'голоса', 'голосов'])})"

                if message['from_id'] == owner_id:
                    api.messages.edit(
                        peer_id=message['peer_id'],
                        message_id=message['id'],
                        message=out_message,
                        disable_mentions=True
                    )
                else:
                    api.messages.send(
                        peer_id=message['peer_id'],
                        random_id=0,
                        message=out_message,
                        disable_mentions=True
                    )

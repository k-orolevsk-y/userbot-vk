import json
import config
import requests
import functions
import ErrorMessages


def cmd(vk, message, args):
    peer_id = message['peer_id']
    _, target = functions.get_user_id_for_message(vk, message, args, ErrorMessages.getMessage('user', '/stickers [пользователь]'))
    stickers_info = json.loads(requests.get(f"https://ssapi.ru/vk-stickers-api/?method=getStickers&user_id={target['id']}").text)
    
    if 'error' in stickers_info:
        return functions.msg_send(
            vk, 
            peer_id, 
            f"{config.prefixes['error']} Ошибка при обращении к API: {stickers_info['error_msg']}",
            message['id'],
            )
    stickers_info = stickers_info['response']
    out_message = f"{config.prefixes['success']} [id{target['id']}|{target['first_name']} {target['last_name']}] имеет {functions.pluralForm(stickers_info['count'], ['стикерпак', 'стикерпака', 'стикерпаков'])}"
    paid_stickers = stickers_info['info']['paid']
    if paid_stickers == 0:
        out_message += ".\n🥺 Платных стикерпаков у пользователя нет."
    else:
        info = stickers_info['info']
        price_votes = info['price_vote']
        price_rubles = info['price']
        out_message += f" из них {functions.pluralForm(paid_stickers, ['стикерпак платный', 'стикерпака платные', 'стикерпаков платные'])} и {functions.pluralForm(info['styles'], ['стиль','стиля','стилей'])}."
        out_message += f"\n\n⚙️ Цена стикеров (в голосах / в рублях): {price_votes} / {price_rubles}₽"

    functions.msg_send(
            vk, 
            peer_id,
            out_message,
            message['id']
    )

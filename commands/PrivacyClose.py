import time
import config
import functions


def cmd(api, message, args, owner_id):
    _type = args[0].lower()[0:2]
    for_all = None if message['from_id'] == message['peer_id'] else True

    if message.get('reply_message') is not None:
        target = api.users.get(
            user_ids=message['reply_message']['from_id'],
        )
    else:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['error']} Необходимо ответить на сообщение пользователя."
        )
        time.sleep(3)
        api.messages.delete(
            message_ids=message['id'],
            delete_for_all=for_all
        )
        return

    target = target[0]
    if target['id'] == owner_id:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['invalid']} Данную команду нельзя использовать на самого себя!"
        )
        time.sleep(3)
        api.messages.delete(
            message_ids=message['id'],
            delete_for_all=for_all
        )
        return

    if _type in ['+музыка', '+audios'] or message['text'] in ['+м', '+a']:
        api_response = api.account.getPrivacySettings()

        owners = []
        for i in range(len(api_response['settings'])):
            if api_response['settings'][i]['key'] != 'audios':
                continue

            try:
                owners = api_response['settings'][i]['value']['owners']['allowed']
            except:
                owners = []

        if not(target['id'] in owners):
            api.messages.edit(
                peer_id=message['peer_id'],
                message_id=message['id'],
                message=f"{config.prefixes['invalid']}️ У пользователя [id{target['id']}|{target['first_name']} {target['last_name']}] нет доступа к аудиозаписям!"
            )

            time.sleep(3)

            api.messages.delete(
                message_ids=message['id'],
                delete_for_all=for_all
            )
            return

        owners.remove(target['id'])
        api.account.setPrivacy(key='audios', value=owners)

        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['success']} Пользователю [id{target['id']}|{target['first_name']} {target['last_name']}] закрыт доступ к аудиозаписям!"
        )
    else:
        api_response = api.account.getPrivacySettings()

        owners = []
        for i in range(len(api_response['settings'])):
            if api_response['settings'][i]['key'] != 'photos_saved':
                continue

            try:
                owners = api_response['settings'][i]['value']['owners']['allowed']
            except:
                owners = []

        if not(target['id'] in owners):
            api.messages.edit(
                peer_id=message['peer_id'],
                message_id=message['id'],
                message=f"{config.prefixes['invalid']}️ У пользователя [id{target['id']}|{target['first_name']} {target['last_name']}] нет доступа к сохрам!"
            )
            time.sleep(3)
            api.messages.delete(
                message_ids=message['id'],
                delete_for_all=for_all
            )
            return

        owners.remove(target['id'])
        api.account.setPrivacy(key='photos_saved', value=owners)

        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['success']} Пользователю [id{target['id']}|{target['first_name']} {target['last_name']}] закрыт доступ к сохрам!"
        )
    return

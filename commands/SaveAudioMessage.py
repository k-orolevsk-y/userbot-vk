import os
import config
import requests
import functions
from vk_api import VkUpload


def cmd(vk, message, args, uploader: VkUpload):
    peer_id = message['peer_id']
    reply = message.get('reply_message')
    for_all = None if message['from_id'] == message['peer_id'] else True

    if reply is None:
        functions.msg_edit(
            vk, peer_id, message['id'],
            f"{config.prefixes['error']} Необходимо ответить на голосовое сообщение.",
            for_all=for_all
        )
        return

    if len(reply['attachments']) < 1:
        functions.msg_edit(
            vk, peer_id, message['id'],
            f"{config.prefixes['error']} Необходимо ответить на голосовое сообщение.",
            for_all=for_all
        )
        return

    if reply['attachments'][0].get('audio_message') is None:
        functions.msg_edit(
            vk, peer_id, message['id'],
            f"{config.prefixes['error']} Необходимо ответить на голосовое сообщение.",
            for_all=for_all
        )
        return

    if len(args) < 2:
        functions.msg_edit(
            vk, peer_id, message['id'],
            f"{config.prefixes['invalid']} Правильное использование: /sa [ключ]",
            for_all=for_all
        )
        return

    data = functions.getData('saved_audio')
    key = str(message['text'].split(' ', 1)[1])

    if data is None:
        data = {}

    if data.get(key) is not None:
        functions.msg_edit(
            vk, peer_id, message['id'],
            f"{config.prefixes['invalid']} Уже есть голосовое сообщение сохранённое под таким ключем!",
            for_all=for_all
        )
        return

    audio = reply['attachments'][0]['audio_message']['link_ogg']
    filename = "files/" + os.path.basename(audio).split('?')[0]
    r = requests.get(audio)
    with open(filename, 'wb') as f:
        f.write(r.content)

    uploaded = uploader.audio_message(audio=filename, peer_id=message['peer_id'])['audio_message']
    os.remove(filename)

    data[key] = f"audio_message{uploaded['owner_id']}_{uploaded['id']}_{uploaded['access_key']}"
    functions.editData('saved_audio', data)

    functions.msg_edit(
        vk, peer_id, message['id'],
        f"{config.prefixes['success']} Голосовое сообщение успешно сохранено под ключем `{key}`!",
        for_all=for_all
    )
    return

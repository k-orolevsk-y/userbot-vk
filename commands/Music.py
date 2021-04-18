import os
import config
import requests
from vk_api import VkUpload

def cmd(api, message, owner_id, uploader: VkUpload):
    attach = message.get('attachments')
    reply = message.get('reply_message')
    if len(attach) == 0 and reply is None:
        api.messages.send(
            peer_id=message['peer_id'],
            random_id=0,
            message=f"{config.prefixes['error']} Необходимо прикрепить аудиозапись или ответить на сообщение с аудиозаписью.",
            reply_to=message['id']
        )
        return

    try:
        if reply is not None:
            _type = reply['attachments'][0]['type']
            if reply['attachments'][0].get('audio') is not None:
                audio = reply['attachments'][0]['audio']['url']
            else:
                raise Exception()
        else:
            audio = attach[0]['audio']['url']
    except:
        api.messages.send(
            peer_id=message['peer_id'],
            random_id=0,
            message=f"{config.prefixes['error']} Необходимо прикрепить аудиозапись или ответить на сообщение с аудиозаписью.",
            reply_to=message['id']
        )
        return

    filename = "files/" + os.path.basename(audio).split('?')[0]
    if len(filename.split('.')) < 2: filename += ".mp3"

    r = requests.get(audio)
    with open(filename, 'wb') as f:
        f.write(r.content)

    if os.path.isfile('files/new_audio.wav'): os.remove('files/new_audio.wav')
    os.system(f"ffmpeg -i {filename} -acodec pcm_s16le -ac 1 -ar 16000 files/new_audio.wav")

    uploaded = uploader.audio_message(filename, message['peer_id'])['audio_message']
    attach = f"audio_message{uploaded['owner_id']}_{uploaded['id']}"

    os.remove(filename)
    os.remove("files/new_audio.wav")

    api.messages.send(
        peer_id=message['peer_id'],
        random_id=0,
        attachment=attach,
        reply_to=None if message['from_id'] == owner_id else message['message_id']
    )
    return

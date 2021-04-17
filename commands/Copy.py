import os
import time
import config
import requests


def cmd(api, message, uploader):
    for_all = None if message['from_id'] == message['peer_id'] else True

    if message.get('reply_message') is None:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['error']} Необходимо ответить на голосовое сообщение."
        )

        time.sleep(3)

        api.messages.delete(
            message_ids=message['id']
        )
        return

    reply = message['reply_message']
    try:
        if reply['attachments'][0]['audio_message'] is not None:
            api.messages.delete(message_ids=message['id'], delete_for_all=for_all)

            gc = reply['attachments'][0]['audio_message']['link_ogg']
            filename = "files/" + os.path.basename(gc).split('?')[0]
            r = requests.get(gc)
            with open(filename, 'wb') as f:
                f.write(r.content)

            uploaded = uploader.audio_message(audio=filename, peer_id=message['peer_id'])['audio_message']
            api.messages.send(peer_id=message['peer_id'], random_id=0,attachment=f"audio_message{uploaded['owner_id']}_{uploaded['id']}")

            os.remove(filename)
        else:
            raise
    except:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['invalid']} Данное сообщение не голосовое."
        )

        time.sleep(3)

        api.messages.delete(
            message_ids=message['id']
        )
    return

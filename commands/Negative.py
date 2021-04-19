import os
import config
import requests
from vk_api import VkUpload


def cmd(api, message, args, uploader: VkUpload):
    attach = message.get('attachments')
    reply = message.get('reply_message')
    if len(attach) == 0 and reply is None:
        api.messages.send(
            peer_id=message['peer_id'],
            random_id=0,
            message=f"{config.prefixes['error']} Необходимо ответить на сообщение с фотографией / стикером, либо прикрепить фотографию.",
            reply_to=message['id']
        )
        return

    try:
        if reply is not None:
            _type = reply['attachments'][0]['type']
            if reply['attachments'][0].get('sticker') is not None:
                img = reply['attachments'][0]['sticker']['images'].pop()['url']
            elif reply['attachments'][0].get('photo') is not None:
                img = reply['attachments'][0]['photo']['sizes'].pop()['url']
            else:
                raise Exception()
        else:
            _type = "photo"
            img = attach[0]['photo']['sizes'].pop()['url']
    except:
        api.messages.send(
            peer_id=message['peer_id'],
            random_id=0,
            message=f"{config.prefixes['error']} Необходимо ответить на сообщение с фотографией / стикером, либо прикрепить фотографию.",
            reply_to=message['id']
        )
        return

    filename = "files/" + os.path.basename(img).split('?')[0]
    if len(filename.split('.')) < 2: filename += ".png"

    r = requests.get(img)
    with open(filename, 'wb') as f:
        f.write(r.content)

    os.system(f"convert {filename} -negate {filename}")

    if _type == "sticker":
        uploaded = uploader.graffiti(filename, peer_id=message['peer_id'])['graffiti']
        attach = f"graffiti{uploaded['owner_id']}_{uploaded['id']}"
    else:
        uploaded = uploader.photo_messages(filename, peer_id=message['peer_id'])[0]
        attach = f"photo{uploaded['owner_id']}_{uploaded['id']}"

    os.remove(filename)
    api.messages.send(
        peer_id=message['peer_id'],
        random_id=0,
        attachment=attach,
        reply_to=message['id']
    )
    return

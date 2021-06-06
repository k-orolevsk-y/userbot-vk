from CustomExceptions import skipHandle
import os
import requests
import functions
import ErrorMessages

from vk_api import VkUpload


def cmd(vk, message, args, uploader: VkUpload):
    attach = message.get('attachments')
    reply = message.get('reply_message')
    peer_id = message['peer_id']
    if len(attach) == 0 and reply is None:
        functions.msg_send(
            vk,
            peer_id,
            ErrorMessages.getMessage('custom', custom_error=('error', ' Необходимо ответить на сообщение с фотографией / стикером, либо прикрепить фотографию.')),
            message['id'],
        )
        raise skipHandle()

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

    filename = "files/" + os.path.basename(img).split('?')[0]
    if len(filename.split('.')) < 2: filename += ".png"

    r = requests.get(img)
    with open(filename, 'wb') as f:
        f.write(r.content)

    if len(args) >= 2:
        prefer_size = args[1]
        if prefer_size.isnumeric():
            prefer_size = int(prefer_size)
            if prefer_size <= 10 and prefer_size >= 1:
                believe_size = 50 - 5*(prefer_size-1)
                size = f'{believe_size}x{believe_size}%'
        else:
            functions.msg_send(
                vk,
                peer_id,
                ErrorMessages.getMessage('correct_use', ' /d [степень от 1 до 10]'),
                message['id']
            )
            raise skipHandle()
    else:
        size = '50x50%'

    os.system(f"convert {filename} -liquid-rescale {size} {filename}")

    if _type == "sticker":
        uploaded = uploader.graffiti(filename, peer_id=message['peer_id'])['graffiti']
        attach = f"graffiti{uploaded['owner_id']}_{uploaded['id']}"
    else:
        uploaded = uploader.photo_messages(filename, peer_id=message['peer_id'])[0]
        attach = f"photo{uploaded['owner_id']}_{uploaded['id']}"
    os.remove(filename)
    
    functions.msg_send(
        vk,
        peer_id,
        attachment=attach,
        reply_to=message['id']
    )
    

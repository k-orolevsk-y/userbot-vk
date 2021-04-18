import os
import config
import requests
from vk_api import VkUpload


def cmd(api, message, args, uploader: VkUpload):
    attach = message.get('attachments')
    if len(attach) == 0 or args[1] is None:
        api.messages.send(
            peer_id=message['peer_id'],
            random_id=0,
            message=f"{config.prefixes['error']} Необходимо прикрепить фотографию и написать текст: /text [text]",
            reply_to=message['id']
        )
        return

    try:
        img = attach[0]['photo']['sizes'].pop()['url']
    except:
        api.messages.send(
            peer_id=message['peer_id'],
            random_id=0,
            message=f"{config.prefixes['error']} Необходимо прикрепить фотографию и написать текст: /text [text]",
            reply_to=message['id']
        )
        return

    filename = "files/" + os.path.basename(img).split('?')[0]
    if len(filename.split('.')) < 2: filename += ".png"

    r = requests.get(img)
    with open(filename, 'wb') as f:
        f.write(r.content)

    text = " ".join(args[1:])
    os.system(f"convert {filename} \
          -bordercolor black -border 3  -bordercolor white -border 2 \
          \( -background black -fill white -pointsize 24 \
             label:\"{text}\"   -trim +repage \
             -bordercolor black -border 30 \
          \) -gravity South -append \
          -bordercolor black -border 10   -gravity South -chop 0x10 \
         {filename}")

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

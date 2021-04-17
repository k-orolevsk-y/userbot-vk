import os
import config
import requests


def cmd(api, message, args, uploader):
    reply = message.get('reply_message')
    if reply is None:
        api.messages.send(
            peer_id=message['peer_id'],
            random_id=0,
            message=f"{config.prefixes['error']} Необходимо ответить на голосовое сообщение.",
            reply_to=message['id']
        )
        return

    if len(reply['attachments']) < 1:
        api.messages.send(
            peer_id=message['peer_id'],
            random_id=0,
            message=f"{config.prefixes['error']} Необходимо ответить на голосовое сообщение.",
            reply_to=message['id']
        )
        return

    if reply['attachments'][0].get('audio_message') is None:
        api.messages.send(
            peer_id=message['peer_id'],
            random_id=0,
            message=f"{config.prefixes['error']} Необходимо ответить на голосовое сообщение.",
            reply_to=message['id']
        )
        return

    audio = reply['attachments'][0]['audio_message']['link_ogg']
    filename = "files/" + os.path.basename(audio).split('?')[0]
    r = requests.get(audio)
    with open(filename, 'wb') as f:
        f.write(r.content)

    if os.path.isfile('files/render1.ogg'): os.remove('files/render1.ogg')
    if os.path.isfile('files/render2.ogg'): os.remove('files/render2.ogg')

    if len(args) >= 2:
        if args[1] == "1":
            os.system(f'ffmpeg -i {filename} -af "chorus=0.5:0.9:50|60|40:0.4|0.32|0.3:0.25|0.4|0.3:2|2.3|1.3" files/render1.ogg')
            os.system(f'ffmpeg -i files/render1.ogg -filter_complex "vibrato=f=15" files/render2.ogg')
        elif args[1] == "2":
            os.system(f'ffmpeg -i {filename} -af "chorus=0.5:0.9:50|60|40:0.4|0.32|0.3:0.25|0.4|0.3:2|2.3|1.3" files/render1.ogg')
            os.system(f'ffmpeg -i files/render1.ogg -filter_complex "vibrato=f=35" files/render2.ogg')
        elif args[1] == "3":
            os.system(f'ffmpeg -i {filename} -af "chorus=0.5:0.9:50|60|40:0.4|0.32|0.3:0.25|0.4|0.3:2|2.3|1.3" files/render1.ogg')
            os.system(f'ffmpeg -i files/render1.ogg -filter_complex "vibrato=f=10" files/render2.ogg')
        elif args[1] == "4":
            os.system(f"ffmpeg -i {filename} -filter_complex \"afftfilt=real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=512:overlap=0.75\" files/render2.ogg")
        else:
            api.messages.send(
                peer_id=message['peer_id'],
                random_id=0,
                message=f"{config.prefixes['invalid']} Использование команды: /audio [1-4]\n1 - стандартный жмых\n2 - сильный жмых\n3 - слабый жмых\n4 - робот",
                reply_to=message['id']
            )
            os.remove(filename)
            return
    else:
        api.messages.send(
            peer_id=message['peer_id'],
            random_id=0,
            message=f"{config.prefixes['invalid']} Использование команды: /audio [1-4]\n1 - стандартный жмых\n2 - сильный жмых\n3 - слабый жмых\n4 - робот",
            reply_to=message['id']
        )
        os.remove(filename)
        return

    uploaded = uploader.audio_message(audio="files/render2.ogg", peer_id=message['peer_id'])['audio_message']
    api.messages.send(
        peer_id=message['peer_id'],
        random_id=0,
        attachment=f"audio_message{uploaded['owner_id']}_{uploaded['id']}",
        reply_to=message['id']
    )

    os.remove(filename)
    if os.path.isfile('files/render1.ogg'): os.remove('files/render1.ogg')
    os.remove('files/render2.ogg')

    return

import time
import config


def cmd(api, message, args, owner_id):
    for_all = None if message['from_id'] == message['peer_id'] else True

    if len(args) < 2 and len(message.get('attachments')) == 0 and message.get('reply_message') is None:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['error']} Необходимо написать сообщение или ответить на стикер / голосовое сообщение."
        )
        time.sleep(1)
        api.messages.delete(
            message_ids=message['id'],
            delete_for_all=for_all
        )
        return

    expire_ttl = 86400
    try:
        last_n = args[1][-1]
        num = int(args[1][0:-1])
        need_more_split = False

        if last_n in ['s', 'с'] and num < 86400:
            need_more_split = True
            expire_ttl = num
        elif last_n in ['m', 'м'] and (num * 60) < 86400:
            need_more_split = True
            expire_ttl = num * 60
        elif last_n in ['h', 'ч'] and (num * 60 * 60) < 86400:
            need_more_split = True
            expire_ttl = num * 60 * 60
    except:
        expire_ttl = 86400
        need_more_split = False

    if not(expire_ttl in [15, 60, 300, 900, 3600, 18000, 86400]):
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['error']} Неверное время исчезающего сообщения, возможные варианты: 15 сек, 1 минута, 5 минут, 15 минут, 1 час, 5 часов, 1 день."
        )
        time.sleep(5)
        api.messages.delete(
            message_ids=message['id'],
            delete_for_all=for_all
        )
        return

    api.messages.edit(
        peer_id=message['peer_id'],
        message_id=message['id'],
        message="&#13;"
    )
    api.messages.delete(
        message_ids=message['id'],
        delete_for_all=for_all
    )

    split_text = message['text'].split(' ', 1)
    if len(split_text) > 1:
        if message.get('reply_message') is not None and message['reply_message']['from_id'] == owner_id:
            if message['reply_message'].get('attachments') is not None:
                if message['reply_message']['attachments'][0].get('type') in ['audio_message', 'sticker']:
                    text = ""
        elif need_more_split:
            text = message['text'].split(' ', 2)[2]
        else:
            text = split_text[1]
    else:
        text = ""

    attachments = []
    for att in message['attachments']:
        att_type = att[att['type']]
        attachment = (
            f"{att['type']}{att_type['owner_id'] if att_type['owner_id'] else att_type['from_id']}_{att_type['id']}")
        attachments.append(attachment)
    attachments = ",".join(attachments)

    reply = None
    fwd_messages = None

    if message.get('reply_message') is not None:
        reply = message['reply_message']['id']
        if len(message['reply_message']['attachments']) > 0 and message['reply_message']['from_id'] == owner_id:
            _type = message['reply_message']['attachments'][0]['type']
            if _type == 'audio_message':
                obj = message['reply_message']['attachments'][0][_type]
                api.messages.delete(message_ids=message['reply_message']['id'], delete_for_all=for_all)
                api.messages.send(
                    peer_id=message['reply_message']['peer_id'],
                    random_id=0,
                    expire_ttl=expire_ttl,
                    attachment=f"audio_message{obj['owner_id']}_{obj['id']}"
                )
                return
            elif _type == 'sticker':
                obj = message['reply_message']['attachments'][0][_type]
                api.messages.delete(message_ids=message['reply_message']['id'], delete_for_all=for_all)
                api.messages.send(
                    peer_id=message['reply_message']['peer_id'],
                    random_id=0,
                    expire_ttl=expire_ttl,
                    sticker_id=f"{obj['sticker_id']}"
                )
                return
    elif message.get('fwd_messages') is not None:
        fwd_messages = ""
        for fwd_msg in message['fwd_messages']:
            fwd_messages += str(fwd_msg.id) + ","
        fwd_messages = fwd_messages[0:-1]

    if text is None:
        mid = api.messages.send(
            peer_id=message['peer_id'],
            random_id=0,
            message=f"{config.prefixes['error']} Необходимо написать сообщение или ответить на стикер / голосовое сообщение."
        )
        time.sleep(1)
        api.messages.delete(
            message_ids=mid,
            delete_for_all=for_all
        )
        return

    api.messages.send(
        peer_id=message['peer_id'],
        random_id=0,
        message=text,
        attachment=attachments,
        expire_ttl=expire_ttl,
        reply_to=reply,
        forward_messages=fwd_messages
    )
    return

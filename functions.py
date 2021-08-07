import re
import json
import time
import ujson
from CustomExceptions import skipHandle


def editData(id_name, newData):
    try:
        file = open('data.json', 'r')
        try:
            data = ujson.loads(file.readline())
        except:
            data = {}
        data[id_name] = newData

        file.close()
        file = open('data.json', 'w')

        file.writelines(ujson.dumps(data))
        file.close()

        return True
    except:
        return False


def getData(id_name):
    try:
        file = open('data.json')
        data = ujson.loads(file.readline())

        return data[str(id_name)]
    except:
        return None


def getUserId(scheme):
    url = re.findall(r'vk\.com/([a-zA-Z0-9_\.]+)', scheme)[0]
    if url is not None:
        return url

    reg = re.findall(r'\[id(\d*)\|.*]', scheme)[0]
    if reg is not None:
        return reg

    return scheme


def get_user_id_for_message(vk, message, args, except_message):
    if message.get('reply_message') is not None:
        user_id = message['reply_message']['from_id']
    else:
        if len(args) < 2:
            msg_send(
                vk,
                message['peer_id'],
                except_message,
                message['id']
            )
            raise skipHandle()

        user_id = getUserId(args[1])

    target = vk.method('users.get', {'user_ids': [user_id]})
    target = target.pop()

    if target is None:
        msg_send(
            vk,
            message['peer_id'],
            except_message,
            message['id']
        )
        raise skipHandle()

    return user_id, target


def pluralForm(amount, variants):
    amount = abs(amount)

    if amount % 10 == 1 and amount % 100 != 11:
        variant = 0
    elif 2 <= amount % 10 <= 4 and (amount % 100 < 10 or amount % 100 >= 20):
        variant = 1
    else:
        variant = 2

    return f"{amount} {variants[variant]}"


def msg_send(vk, peer_id, message=None, reply_to=None, disable_mentions=0, attachment=None, keybrd=None, fvd=None,
             parse_links=0, forward=None, content_source=None):
    if content_source is not None:
        content_source = json.dumps(content_source)
    return vk.method('messages.send',
                     {'peer_id': peer_id,
                      'message': message,
                      'attachment': attachment,
                      'keyboard': keybrd,
                      'forward_messages': fvd,
                      'reply_to': reply_to,
                      'dont_parse_links': parse_links,
                      'forward': forward,
                      'content_source': content_source,
                      'disable_mentions': disable_mentions,
                      'random_id': 0})


def msg_edit(vk, peer_id, message_id, message=None, attachment=None, sleeping=3, for_all=None):
    vk.method('messages.edit',
              {'peer_id': peer_id,
               'message_id': message_id,
               'message': message,
               'attachment': attachment
               })
    if sleeping is not None:
        time.sleep(sleeping)
        vk.method('messages.delete', {
            'message_ids': [message_id],
            'delete_for_all': for_all
        })
    return True

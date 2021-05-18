import re
import ujson
import random
import json
import urllib.parse
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
    try:
        parse = urllib.parse.urlparse(scheme).path
        if scheme is not parse:
            parse = str(parse)
            return parse if parse[1] != "/" else parse[1:]

        reg = re.findall(r'\[id(\d*)\|.*]', scheme)[0]
        if reg is not None:
            return reg

        return scheme
    except:
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


def msg_send(vk, peer_id, message=None, reply_to=None, disable_mentions=0, attachment=None, keybrd=None, fvd=None, parse_links=0, forward=None, content_source=None):
        if content_source is not None:
            content_source = json.dumps(content_source)
        rand = random.randint(0, 9999999999999999999999999999999)
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
                         'random_id': rand})
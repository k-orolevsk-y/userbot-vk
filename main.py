import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
from threading import Thread
import os
import time
import config
import functions

from commands import Audio
from commands import Ban
from commands import BanChat
from commands import Copy
from commands import Delete
from commands import Dist
from commands import Help
from commands import Ignore
from commands import InvisibleMessage
from commands import Music
from commands import Negative
from commands import PrivacyClose
from commands import PrivacyOpen
from commands import Repeat
from commands import TestersCheck
from commands import Text
from commands import UnBan
from commands import UnBanChat
from commands import UnIgnore
from commands import UserId

if config.access_token is None or config.access_token == "":
    exit("Необходимо установить access_token в config.py")

vk_session = vk_api.VkApi(token=config.access_token)
api = vk_session.get_api()
uploader = VkUpload(vk_session)

longpoll = VkLongPoll(vk_session)
owner_id = api.users.get()[0]['id']

os.system(f"renice -n 20 -p {os.getpid()}")
if not os.path.exists('data.json'):
    file = open('data.json', "w")
    file.writelines("{}")
    file.close()
if not os.path.isdir("files"):
    os.mkdir("files")
    os.system("chmod 777 files")

user_names_cache = {}
group_names_cache = {}
chat_names_cache = {}


def getUserName(user_id):
    if user_id < 0 and group_names_cache.get(abs(user_id)) is None:
        group = api.groups.getById(group_id=(abs(user_id)))[0]
        group_names_cache[group['id']] = group['name']

        return group['name']
    elif user_id < 0:
        return group_names_cache[abs(user_id)]

    if user_names_cache.get(user_id) is None:
        user = api.users.get(user_ids=user_id)[0]
        user_names_cache[user['id']] = f"{user['first_name']} {user['last_name']}"

    return user_names_cache.get(user_id)


def getChatName(chat_id):
    if chat_names_cache.get(chat_id) is None:
        chat = api.messages.getChatPreview(peer_id=chat_id)
        chat_names_cache[chat_id] = chat['preview']['title']

    return chat_names_cache.get(chat_id)


print("Успешный запуск бота.")
try:
    for event in longpoll.listen():
        if event.type != VkEventType.MESSAGE_NEW:
            continue

        message = api.messages.getById(message_ids=event.message_id)['items'][0]
        th = None

        if config.log_messages:
            current_time = time.strftime("%H:%M:%S", time.localtime())

            text = event.message.replace('\n', ' ')
            if text is None or text == "":
                if len(message.get('attachments')) > 0:
                    text = str(message.get('attachments')[0]['type'])
                    replacer = {
                        'audio_message': '• голосовое сообщение',
                        'audio': '• аудиозапись',
                        'sticker': '• стикер',
                        'photo': '• фотография',
                        'video': '• видео',
                        'doc': '• документ',
                        'graffiti': '• граффити'
                    }  # TODO: доработать (добавить ссылки на содержимое)

                    for replace in replacer:
                        text = text.replace(replace, replacer[replace])
                else:
                    text = "• пересланные сообщения"

            if message['peer_id'] > 2000000000:
                print(f"\033[34m[{current_time}] "
                      f"\033[37m[\033[32m{getChatName(message['peer_id'])}\033[37m/\033[31m{getUserName(message['from_id'])}\033[37m]: \033[36m{text}")
            else:
                print(f"\033[34m[{current_time}] "
                      f"\033[37m[ЛС] [\033[32m{getUserName(message['peer_id'])}\033[37m/\033[31m{getUserName(message['from_id'])}\033[37m]: \033[36m{text}")

        ignored_users = functions.getData('ignore')
        if ignored_users is not None:
            if message['from_id'] in ignored_users:
                api.messages.delete(
                    message_ids=message['id'],
                    delete_for_all=0
                )
                continue

        banned = functions.getData('banned')
        if banned is not None:
            if message['from_id'] in banned:
                continue

        banned_peers = functions.getData('banned_peers')
        if banned_peers is not None:
            if (message['peer_id'] in banned_peers) and not (message['from_id'] == owner_id):
                continue

        args = message['text'].split(" ")
        if message['from_id'] == owner_id:
            if args[0].lower() == '/copy':
                th = Thread(target=Copy.cmd, args=(api, message, uploader))
            elif args[0].lower() == '/del':
                th = Thread(target=Delete.cmd, args=(api, message, args, owner_id))
            elif args[0].lower() in ['/i', '/и']:
                th = Thread(target=InvisibleMessage.cmd, args=(api, message, args, owner_id))
            elif args[0].lower() == '/repeat':
                th = Thread(target=Repeat.cmd, args=(api, message, args))
            elif args[0].lower() == '/ban':
                th = Thread(target=Ban.cmd, args=(api, message, args, owner_id))
            elif args[0].lower() == '/ban_chat':
                th = Thread(target=BanChat.cmd, args=(api, message, args))
            elif args[0].lower() == '/unban':
                th = Thread(target=UnBan.cmd, args=(api, message, args))
            elif args[0].lower() == '/unban_chat':
                th = Thread(target=UnBanChat.cmd, args=(api, message))
            elif args[0].lower() == '/ignore':
                th = Thread(target=Ignore.cmd, args=(api, message, args, owner_id))
            elif args[0].lower() == '/unignore':
                th = Thread(target=UnIgnore.cmd, args=(api, message, args))
            elif args[0].lower()[0:2] in ['+музыка', '+audios', '+сохры', '+saves'] \
                    or args[0].lower() in ['+м', '+a', '+с', '+s']:
                th = Thread(target=PrivacyOpen.cmd, args=(api, message, args, owner_id))
            elif args[0].lower()[0:2] in ['-музыка', '-audios', '-сохры', '-saves'] \
                    or args[0].lower() in ['-м', '-a', '-с', '-s']:
                th = Thread(target=PrivacyClose.cmd, args=(api, message, args, owner_id))

        if args[0].lower() in ['/au', '/audio']:
            th = Thread(target=Audio.cmd, args=(api, message, args, uploader))
        elif args[0].lower() in ['/d', '/dist']:
            th = Thread(target=Dist.cmd, args=(api, message, args, uploader))
        elif args[0].lower() in ['/n', '/negative']:
            th = Thread(target=Negative.cmd, args=(api, message, args, uploader))
        elif args[0].lower() in ['/t', '/text']:
            th = Thread(target=Text.cmd, args=(api, message, args, uploader))
        elif args[0].lower() in ['/tc', '/tester_check']:
            th = Thread(target=TestersCheck.cmd, args=(api, message, args, owner_id))
        elif args[0].lower() in ['/ma', '/music_audio']:
            th = Thread(target=Music.cmd, args=(api, message, owner_id, uploader))
        elif args[0].lower() in ['/userid', '/uid']:
            th = Thread(target=UserId.cmd, args=(api, message, args))
        elif args[0].lower() in ['/help', '/911', '/112']:
            th = Thread(target=Help.cmd, args=(api, message, owner_id))

        if th is not None:
            th.start()
            th = None
except:
    print("")

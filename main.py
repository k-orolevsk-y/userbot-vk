import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
import config
import functions
import time
import os

from commands import Copy
from commands import Delete
from commands import Audio
from commands import Dist
from commands import InvisibleMessage
from commands import TestersCheck
from commands import Repeat
from commands import Music
from commands import Ban
from commands import BanChat
from commands import UnBan
from commands import UnBanChat
from commands import UserId
from commands import Ignore
from commands import UnIgnore
from commands import PrivacyOpen
from commands import PrivacyClose


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
chat_names_cache = {}


def getUserName(user_id):
    if user_id < 0:
        return f"Группа {user_id}"

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
for event in longpoll.listen():
    if event.type != VkEventType.MESSAGE_NEW:
        continue

    message = api.messages.getById(message_ids=event.message_id)['items'][0]
    if config.log_messages:
        current_time = time.strftime("%H:%M:%S", time.localtime())

        text = event.message.replace('\n', ' ')
        if text is None or text == "":
            if len(message.get('attachments')) > 0:
                text = str(message.get('attachments')[0]['type'])
                replacer = {
                    'audio_message': '• голосовое сообщение',
                    'audio': '• песня',
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

        if event.peer_id > 2000000000:
            print(f"\033[34m[{current_time}] "
                  f"\033[37m[\033[32m{getChatName(message['peer_id'])}\033[37m/\033[31m{getUserName(message['from_id'])}\033[37m]: \033[36m{text}")
        elif event.peer_id < 0:
            continue
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
            Copy.cmd(api, message, uploader)
        elif args[0].lower() == '/del':
            Delete.cmd(api, message, args, owner_id)
        elif args[0].lower() in ['/i', '/и']:
            InvisibleMessage.cmd(api, message, args, owner_id)
        elif args[0].lower() == '/repeat':
            Repeat.cmd(api, message, args)
        elif args[0].lower() == '/ban':
            Ban.cmd(api, message, args, owner_id)
        elif args[0].lower() == '/ban_chat':
            BanChat.cmd(api, message, args)
        elif args[0].lower() == '/unban':
            UnBan.cmd(api, message, args)
        elif args[0].lower() == '/unban_chat':
            UnBanChat.cmd(api, message)
        elif args[0].lower() == '/ignore':
            Ignore.cmd(api, message, args, owner_id)
        elif args[0].lower() == '/unignore':
            UnIgnore.cmd(api, message, args)
        elif args[0].lower()[0:2] in ['+музыка', '+audios', '+сохры', '+saves'] \
                or args[0].lower() in ['+м', '+a', '+с', '+s']:
            PrivacyOpen.cmd(api, message, args, owner_id)
        elif args[0].lower()[0:2] in ['-музыка', '-audios', '-сохры', '-saves'] \
                or args[0].lower() in ['-м', '-a', '-с', '-s']:
            PrivacyClose.cmd(api, message, args, owner_id)

    if args[0].lower() == '/audio':
        Audio.cmd(api, message, args, uploader)
    elif args[0].lower() == '/d':
        Dist.cmd(api, message, args, uploader)
    elif args[0].lower() in ['/tc', '/tester_check']:
        TestersCheck.cmd(api, message, args, owner_id)
    elif args[0].lower() in ['/ma', '/music_audio']:
        Music.cmd(api, message, owner_id, uploader)
    elif args[0].lower() in ['/userid', '/uid']:
        UserId.cmd(api, message, args)

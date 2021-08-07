import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
from threading import Thread
import os
import time
import functions
from termcolor import colored
from commands import *
from CustomExceptions import *
import config

try:
    import config_local as config
except ImportError:
    pass

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


def worker(event):
    try:
        message = api.messages.getById(message_ids=event.message_id)['items'][0]

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
                        'graffiti': '• граффити',
                        'link': '• ссылка'
                    }  # TODO: доработать (добавить ссылки на содержимое)

                    for replace in replacer:
                        text = text.replace(replace, replacer[replace])
                else:
                    text = "• пересланные сообщения"

            prep_time = colored(f"[{current_time}]", 'blue')
            mark = ''
            user_ask = colored(getUserName(message['from_id']), 'red')
            prep_text = ": " + colored(text, 'cyan')

            if message['peer_id'] > 2000000000:
                conversation = colored(getChatName(message['peer_id']), 'green')
            else:
                conversation = colored(getUserName(message['peer_id']), 'green')
                mark = "[ЛС]"

            info_conversation = f"[{conversation}/{user_ask}]{prep_text}"
            print(
                prep_time,
                mark,
                info_conversation,
            )

        ignored_users = functions.getData('ignore')
        if ignored_users is not None:
            if message['from_id'] in ignored_users:
                api.messages.delete(
                    message_ids=message['id'],
                    delete_for_all=0
                )
                raise skipHandle()

        banned = functions.getData('banned')
        if banned is not None:
            if message['from_id'] in banned:
                raise skipHandle()

        banned_peers = functions.getData('banned_peers')
        if banned_peers is not None:
            if (message['peer_id'] in banned_peers) and not (message['from_id'] == owner_id):
                raise skipHandle()

        disable = functions.getData('disabled')
        if disable and message['from_id'] != owner_id:
            raise skipHandle()

        if message['text'] is None or message['text'] == "":
            raise skipHandle()

        args = message['text'].split()
        cmd = args[0].lower()

        if message['from_id'] == owner_id:
            if cmd == '/copy':
                Copy.cmd(api, message, uploader)
            elif cmd == '/del':
                Delete.cmd(api, message, args, owner_id)
            elif cmd in ['/i', '/и']:
                InvisibleMessage.cmd(api, message, args, owner_id)
            elif cmd == '/repeat':
                Repeat.cmd(api, message, args)
            elif cmd == '/ban':
                Ban.cmd(api, message, args, owner_id)
            elif cmd == '/ban_chat':
                BanChat.cmd(api, message, args)
            elif cmd == '/unban':
                UnBan.cmd(api, message, args)
            elif cmd == '/unban_chat':
                UnBanChat.cmd(api, message)
            elif cmd == '/ignore':
                Ignore.cmd(api, message, args, owner_id)
            elif cmd == '/unignore':
                UnIgnore.cmd(api, message, args)
            elif cmd == '/disable':
                Disable.cmd(api, message)
            elif cmd in ['/sa', '/save_audio']:
                SaveAudioMessage.cmd(vk_session, message, args, uploader)
            elif cmd in ['/ag', '/aget']:
                GetSavedAudioMessage.cmd(vk_session, message, args)
            elif cmd in ['/ad', '/adelete']:
                DeleteSavedAudioMessage.cmd(vk_session, message, args)
            elif cmd in ['/alist']:
                ListSavedAudioMessage.cmd(vk_session, message, args)
            elif cmd in ['+музыка', '+audios', '+сохры', '+saves', '+м', '+a', '+с', '+s']:
                PrivacyOpen.cmd(api, message, args, owner_id)
            elif cmd in ['-музыка', '-audios', '-сохры', '-saves', '-м', '-a', '-с', '-s']:
                PrivacyClose.cmd(api, message, args, owner_id)

        if cmd in ['/au', '/audio']:
            Audio.cmd(api, message, args, uploader)
        elif cmd in ['/d', '/dist']:
            Dist.cmd(vk_session, message, args, uploader)
        elif cmd in ['/n', '/negative']:
            Negative.cmd(api, message, args, uploader)
        elif cmd in ['/t', '/text']:
            Text.cmd(api, message, args, uploader)
        elif cmd in ['/tc', '/tester_check']:
            TestersCheck.cmd(api, message, args)
        elif cmd in ['/stickers', '/st']:
            Stickers.cmd(vk_session, message, args)
        elif cmd in ['/ma', '/music_audio']:
            Music.cmd(api, message, owner_id, uploader)
        elif cmd in ['/userid', '/uid']:
            UserId.cmd(api, message, owner_id, args)
        elif cmd in ['/help', '/911', '/112']:
            Help.cmd(api, message, owner_id)

    except skipHandle:
        pass
    except Exception as e:
        print(e)


print("Успешный запуск бота.")
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        multiprocess_worker = Thread(target=worker, args=(event,))
        multiprocess_worker.start()

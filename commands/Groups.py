import time

import requests

import config
import functions


def get_token(api, message):
    resp = functions.getData('odeanon_token')
    if resp is not None:
        return resp
    else:
        config.odeanon_token = True
        try:
            api.messages.edit(
                peer_id=message['peer_id'],
                message_id=message['id'],
                message=f"{config.prefixes['process']} Идёт получение токена"
            )
        except:
            pass
        api.messages.send(
            peer_id='-197641192',
            random_id=0,
            message='/api reset'
        )
        while True:
            time.sleep(1)
            print("While in progress")
            if functions.getData('odeanon_token') is None:
                continue
            else:
                config.odeanon_token = False
                return functions.getData('odeanon_token')


def cmd(api, message, args, owner_id):
    reply = message.get('reply_message')
    tkn = get_token(api, message)
    progress = True

    if reply is not None:
        user_id = message['reply_message']['from_id']

    else:
        if len(args) < 2:
            if message['from_id'] == owner_id:
                api.messages.edit(
                    peer_id=message['peer_id'],
                    message_id=message['id'],
                    message=f"{config.prefixes['error']} Правильное использование: /groups [пользователь]"
                )
            else:
                api.messages.send(
                    peer_id=message['peer_id'],
                    random_id=0,
                    message=f"{config.prefixes['error']} Правильное использование: /groups [пользователь]"
                )
            progress = False
        else:
            user_id = functions.getUserId(args[1])

    if progress:
        target = api.users.get(
            user_ids=user_id
        )[0]

        groups_info = requests.get(
            f"https://api.korolevsky.me/method/groups.get?access_token={tkn}&user_id={target['id']}"
        ).json()

        out_message = ''

        if not groups_info['ok']:
            out_message += f"{config.prefixes['error']} " \
                           f"В душе блять не ебу че произошло, мне ошибки не дали, мне похуй"

            if message['from_id'] == owner_id:
                api.messages.edit(
                    peer_id=message['peer_id'],
                    message_id=message['id'],
                    message=out_message
                )
            else:
                api.messages.send(
                    peer_id=message['peer_id'],
                    random_id=0,
                    message=out_message
                )

        elif groups_info['ok']:
            groups_info = groups_info['response']
            groups_items = groups_info['items']

            out_message += f"[id{message['from_id']}|✅] | " \
                           f"Группы [id{target['id']}|{target['first_name']} {target['last_name']}] "

            vk_count = 0
            vk_groups = []

            for i in groups_items:
                if vk_count < 250:
                    vk_count += 1
                    vk_groups.append(str(i['group_id']))

            vk_groups = ",".join(vk_groups)

            vk_resp = api.groups.getById(
                group_ids=vk_groups,
                fields="members_count"
            )

            print(vk_resp)

            vk_count = 0
            vk_groups = {}

            for i in vk_resp:
                vk_count += 1
                vk_groups[vk_count] = i['members_count']

            groups = ""
            count = 0

            for i in groups_items:
                if len(groups) < 3000:
                    count += 1
                    groups += f"{count}. [club{i['group_id']}|{i['name']}] (👥 {vk_groups[count]})\n"

            out_message += f"(показано {count}/{groups_info['count']})\n\n{groups}"

            if message['from_id'] == owner_id:
                api.messages.edit(
                    peer_id=message['peer_id'],
                    message_id=message['id'],
                    message=out_message
                )
            else:
                api.messages.send(
                    peer_id=message['peer_id'],
                    random_id=0,
                    message=out_message
                )

import config
import functions


def cmd(vk, message):
    peer_id = message['peer_id']
    for_all = None if message['from_id'] == message['peer_id'] else True

    audios = functions.getData('saved_audio')
    if audios is None or len(audios) < 1:
        functions.msg_edit(
            vk, peer_id, message['id'],
            f"{config.prefixes['invalid']} У Вас нет сохранённых голосовых сообщений.",
            for_all=for_all
        )
        return

    names = []
    for audio in audios.keys():
        names.append(audio)

    functions.msg_edit(
        vk, peer_id, message['id'],
        f"📖 Сохранённые голосовые сообщения: {', '.join(names)}", sleeping=None
    )
    return

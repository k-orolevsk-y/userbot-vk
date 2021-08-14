import config
import functions


def cmd(vk, message):
    peer_id = message['peer_id']
    for_all = None if message['from_id'] == message['peer_id'] else True

    assocs = functions.getData('assoc')
    if assocs is None or len(assocs) < 1:
        functions.msg_edit(
            vk, peer_id, message['id'],
            f"{config.prefixes['invalid']} У Вас нет ассоциаций.",
            for_all=for_all
        )
        return

    sort = {}
    for assoc in assocs.keys():
        if sort.get(assocs[assoc]) is None:
            sort[assocs[assoc]] = []

        sort[assocs[assoc]].append(assoc)

    names = []
    for assoc in sort.keys():
        names.append(f"{assoc}: {', '.join(sort[assoc])}")

    functions.msg_edit(
        vk, peer_id, message['id'],
        f"📖 Ассоциации:<br>{';<br>'.join(names)}", sleeping=None
    )
    return

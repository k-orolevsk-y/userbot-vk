import time
import config
import functions


def cmd(api, message):
    for_all = None if message['from_id'] == message['peer_id'] else True

    disabled = functions.getData("disabled")
    if disabled:
        functions.editData('disabled', False)

        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['success']} Общедоступные функции были успешно включены!"
        )
        time.sleep(3)
        api.messages.delete(
            message_ids=message['id'],
            delete_for_all=for_all
        )
    else:
        functions.editData('disabled', True)

        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['success_no']} Общедоступные функции были успешно отключены!"
        )
        time.sleep(3)
        api.messages.delete(
            message_ids=message['id'],
            delete_for_all=for_all
        )

    return

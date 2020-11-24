def message_data_mod(client, type_, author_id, message_id, data=None):
    if type_ == "add":
        try:
            client.msg_data[author_id].append((message_id, data))
        except KeyError:
            client.msg_data[author_id] = []
            client.msg_data[author_id].append((message_id, data))
        return True

    elif type_ == "remove":
        try:
            correct_data = ()
            for data in client.msg_data[author_id]:
                if data[0] == message_id:
                    correct_data = data
                    break
            if not correct_data:
                return False

            client.msg_data[author_id].remove(correct_data)
            return correct_data[1]
        except KeyError:
            return False

    elif type_ == "list":
        return client.msg_data[author_id]

    else:
        raise Exception(f"Invalid type of '{type_}'!")


class bot():
    def __init__(self):
        pass


client = bot()
client.msg_data = {}




print(message_data_mod(client, "add", 69, 420, "gban"))
print(message_data_mod(client, "add", 69, 421, "npoll"))
print(message_data_mod(client, "add", 70, 422, "spoll"))

print(client.msg_data)

print(message_data_mod(client, "remove", 69, 420))
print(message_data_mod(client, "remove", 70, 421))
print(message_data_mod(client, "remove", 69, 422))

print(client.msg_data)

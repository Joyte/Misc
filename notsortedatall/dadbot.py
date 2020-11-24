from discord.ext import commands

prefix = "."
client = commands.Bot(command_prefix=prefix)
client.remove_command("help")

botToken = "NzczMDc3NTM0NzY5Njc2Mjkw.X6D-jw.muFqgRN1PQBiDKPGCsNUXsp_ai4"


@client.event
async def on_ready():
    print(f"Logged in as the bot ({client.user})!")


@client.event
async def on_message(message):
    print(message.author.id)
    if message.author.id == 773077534769676290:
        return

    print(message.content)

    msg = message.content.lower()
    orig = msg
    if " i'm " in msg or " im " in msg or "im " in msg or "i'm " in msg:
        msg = msg.split(" i'm ", 0)
        if msg == orig:
            msg = msg.split(" im ", 0)
        if msg == orig:
            msg = msg.split("i'm ", 0)
        if msg == orig:
            msg = msg.split("im ", 0)

        print(msg)

        try:
            msg = msg[1]
        except IndexError:
            msg = msg[0]

        print(msg)

        if msg[0] == " ":
            msg = list(msg)
            msg.pop(0)
            msg = "".join(msg)

        print(msg)

        front = msg[0] + msg[1]
        if front == "im":
            front = list(front)
            front.pop(0)
            front.pop(0)
            front = "".join(front)
        elif front == "i'm":
            front = list(front)
            front.pop(0)
            front.pop(0)
            front.pop(0)
            front = "".join(front)

        print(msg)

        await message.channel.send(f"Hi {front}, i'm dad!")


client.run(botToken)

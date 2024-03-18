import asyncio
import cowsay

ALL_VALID_NAMES = set(cowsay.list_cows())
clients = {}
accounts = {}

async def parse_the_command(data, me):
    if data:
        match data[0]:
            case 'who':
                await clients[me].put(f'Logged users:\n{"\n".join(list(accounts.values()))}')
            case 'cows':
                await clients[me].put(sorted(ALL_VALID_NAMES - set(accounts.values())))
            case 'login':
                if len(data) == 1:
                    await clients[me].put('Login name is required (use "cows" to show unused names)')
                elif len(data) > 2:
                    await clients[me].put('Invalid arguments. Use login <cow_name>')
                else:
                    if data[1] not in ALL_VALID_NAMES:
                        await clients[me].put('Invalid cow`s name')
                    elif data[1] in accounts.values():
                        await clients[me].put('Specified login already exists')
                    else:
                        accounts[me] = data[1]
                        await clients[me].put(f'You are logged in as {data[1]}')
            case 'say':
                if me not in accounts.keys():
                    await clients[me].put('You should log in')
                    return 0
                if len(data) != 2:
                    await clients[me].put('User name and text message are required. Use "say <destination_name> <text_message>"')
                else:
                    if ' ' in data[1]:
                        user, msg = data[1].split(maxsplit=1)
                        if user in accounts.values():
                            if user == accounts[me]:
                                await clients[me].put('You are sending the message to yourself')
                            rec = [c for c, v in accounts.items() if v == user][0]
                            await clients[rec].put(cowsay.cowsay(msg, cow=accounts[me]))
                        else:
                            await clients[me].put(f'User {user} doesnt exist or offline')
                    else:
                        await clients[me].put('Text message is missing')
            case 'yield':
                if me not in accounts.keys():
                    await clients[me].put('You should log in')
                    return 0
                if len(data) != 2:
                    await clients[me].put('Text message is required. Use "yield <text_message>"')
                else:
                    for i, j in clients.items():
                        if i in accounts.keys() and j is not clients[me]:
                            await j.put(cowsay.cowsay(data[1], cow=accounts[me]))
            case 'quit' | 'q':
                if me in accounts:
                    del accounts[me]
                elif me in clients:
                    del clients[me]
                    return 1
            case _:
                await clients[me].put('Invalid command')

async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                data = q.result().decode().strip().split(maxsplit=1)
                answer = await parse_the_command(data, me)
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
        if answer:
            break
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())


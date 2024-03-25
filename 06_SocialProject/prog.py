import asyncio
import cowsay

ALL_VALID_NAMES = set(cowsay.list_cows())
accounts = {}

async def chat(reader, writer):
    while not reader.at_eof():
        data = (await reader.readline()).decode().strip().split(maxsplit=1)
        if data:
            match data[0]:
                case 'who':
                    writer.write(f'Logged users:\n{"\n".join(list(accounts.keys()))}'.encode() + b'\n')
                case 'cows':
                    writer.write('\n'.join(list(sorted(ALL_VALID_NAMES - set(accounts.values())))).encode() + b'\n')
                case 'login':
                    if len(data) == 1:
                        writer.write('Login name is required (use "cows" to show unused names)\n'.encode())
                    elif len(data) > 2:
                        writer.write('Invalid arguments. Use login <cow_name>\n'.encode())
                    else:
                        if data[1] not in ALL_VALID_NAMES:
                            writer.write('Invalid cow`s name\n'.encode())
                        elif data[1] in accounts.values():
                            writer.write('Specified login already exists\n'.encode())
                        else:
                            accounts[data[1]] = writer
                            writer.write(f'You are logged in as {data[1]}\n'.encode())
                case 'say':
                    if user is None:
                        writer.write('You should log in\n'.encode())
                        return 0
                    if len(data) != 2:
                        writer.write('User name and text message are required. Use "say <destination_name> <text_message>"\n'.encode())
                    else:
                        if ' ' in data[1]:
                            cow, msg = data[1].split(maxsplit=1)
                            if cow in accounts.values():
                                if user == accounts[cow]:
                                    writer.write('You are sending the message to yourself'.encode())
                                wrtr = accounts[cow]
                                wrtr.writer(cowsay.cowsay(msg, cow=accounts[me]).encode() + b'\n')
                                await wrtr.drain()
                            else:
                                writer.write(f'User {user} doesnt exist or offline'.encode() + b'\n')
                        else:
                            writer.write('Text message is missing\n'.encode())
                case 'yield':
                    if user is None:
                        writer.write('You should log in\n'.encode())
                    if len(data) != 2:
                        writer.write('Text message is required. Use "yield <text_message>"\n'.encode())
                    else:
                        for i, j in accounts.items():
                            if j is not None:
                                writer.write(cowsay.cowsay(data[1], cow=accounts[me]).encode() + b'\n')
                                await writer.drain()
                case 'quit' | 'q':
                    if user is not None:
                        del accounts[user]
                    break
                case _:
                    writer.write('Invalid command\n'.encode())
            await writer.drain()
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())


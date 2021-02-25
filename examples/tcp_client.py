import asyncio
import aiosub


class Protocol(asyncio.Protocol):
    pass


async def main():
    loop = asyncio.get_running_loop()
    message = 'Hello World!'
    protocol = Protocol()
    events = aiosub.subscribe(protocol)
    transport, _ = await loop.create_connection(lambda: protocol, '127.0.0.1', 8888)
    while True:
        event = await events.get()
        if event.name == 'connection_made':
            transport.write(message.encode())
        elif event.name == 'data_received':
            message = event.args['data'].decode()
            print(message)
        elif event.name == 'connection_lost':
            break
    transport.close()

asyncio.run(main())

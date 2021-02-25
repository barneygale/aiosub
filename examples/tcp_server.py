import asyncio
import aiosub


class Protocol(asyncio.Protocol):
    pass


async def conn(events):
    transport = None
    while True:
        event = await events.get()
        if event.name == 'connection_made':
            transport = event.args['transport']
        elif event.name == 'data_received':
            message = event.args['data'].decode()
            print(message)
            transport.write(message.encode())
            transport.close()
        elif event.name == 'connection_lost':
            break


async def main():
    loop = asyncio.get_running_loop()
    def factory():
        protocol = Protocol()
        events = aiosub.subscribe(protocol)
        asyncio.Task(conn(events))
        return protocol
    server = await loop.create_server(factory, '127.0.0.1', 8888)
    async with server:
        await server.serve_forever()


asyncio.run(main())

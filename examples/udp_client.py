import asyncio
import aiosub


class Protocol(asyncio.DatagramProtocol):
    pass


async def main():
    loop = asyncio.get_running_loop()
    message = 'Hello World!'
    protocol = Protocol()
    events = aiosub.subscribe(protocol)
    transport, _ = await loop.create_datagram_endpoint(lambda: protocol, remote_addr=('127.0.0.1', 9999))
    while True:
        event = await events.get()
        if event.name == 'connection_made':
            transport.sendto(message.encode())
        elif event.name == 'datagram_received':
            message = event.args['data'].decode()
            print(message)
            transport.close()
        elif event.name == 'connection_lost':
            break
    transport.close()

asyncio.run(main())
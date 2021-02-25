import asyncio
import aiosub


class Protocol(asyncio.DatagramProtocol):
    pass


async def main():
    loop = asyncio.get_running_loop()
    protocol = Protocol()
    events = aiosub.subscribe(protocol)
    transport, _ = await loop.create_datagram_endpoint(lambda: protocol, local_addr=('127.0.0.1', 9999))
    while True:
        event = await events.get()
        if event.name == 'datagram_received':
            message = event.args['data'].decode()
            addr = event.args['addr']
            print(message)
            transport.sendto(message.encode(), addr)
        elif event.name == 'connection_lost':
            break


asyncio.run(main())

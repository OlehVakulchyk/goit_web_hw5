import platform

import asyncio
import logging
import websockets
import names
from datetime import datetime
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
from aiofile import async_open
from aiopath import AsyncPath

from currency_pb import course, adapter_data

logging.basicConfig(level=logging.INFO)


async def write_log(message: str, name: str):
          
    async with async_open("exchange.log", 'a') as ex:
        date = datetime.now()
        await ex.write(f"{date}  {AsyncPath(__file__)} '{message}' from {name}\n")
    


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            if message.startswith('exchange'):
                await write_log(message, ws.name)
                days = 1
                args_currency = message.split()
                if (len(args_currency) == 2 and 
                    args_currency[1].isdigit()
                    ):
                    days = int(args_currency[1])
                    if days > 10:
                        logger.info(f'second argumrnt in *{message}* must be less 10')
                        days = 1
                else:
                    logging.info(f'current exchange rate for today')
                message += ' Privat'
                if platform.system() == "Windows":
                    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
                    data = await course(days)
                    for r in data:
                        result = adapter_data(r)
#                        result = '; '.join([f'{key.capitalize()}: {value}' for key, value in dictionary[0].items()])
                        message = message + ' *-*-* ' + str(result)
                await self.send_to_clients(f"{ws.name}: {message}")
            else:
                await self.send_to_clients(f"{ws.name}: {message}")


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever
    

if __name__ == '__main__':
    asyncio.run(main())
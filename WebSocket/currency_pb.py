from datetime import datetime
from datetime import timedelta

import aiohttp
import asyncio

CURRENCIES = ["EUR", "USD", "CHF", "CZK", "GBP", "PLN"]


def adapter_data(data: list[dict]):
    
    result = [
        {
            f"{el.get('currency')}": {
                "sale": float(el.get("saleRate")),
                "buy": float(el.get("purchaseRate")),
            }
        }
        for el in data.get("exchangeRate")
        if el.get("currency") in CURRENCIES
    ]
    return [{'date': data.get("date")}] + result

async def currency_exchange_rate(session, date_exchange):
    url = "https://api.privatbank.ua/p24api/exchange_rates?json&date=" + date_exchange
    try:
        async with session.get(url) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result
                    else:
                        print(f"Error status: {response.status} for {url}")
    except aiohttp.ClientConnectorError as err:
        print(f'Connection error: {url}', str(err))
                    

async def course(days=1):
    now = datetime.now()            # current date and time
    async with aiohttp.ClientSession() as session:
        r=[]
        for i in range(days):            
            date_type_i = now.date() - timedelta(i)
            date_r_i = date_type_i.strftime("%d.%m.%Y")
            r.append(currency_exchange_rate(session, date_r_i))           
        return await asyncio.gather(*r)

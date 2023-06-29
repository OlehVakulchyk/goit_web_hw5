import platform

import argparse
from datetime import datetime
from datetime import timedelta

import aiohttp
import asyncio


def pretty_view(data: list[dict]):
    sorted_data = sorted(data, key=lambda x:list(x.keys())[0])
    pattern = "|{:^10}|{:^10}|{:^10}|"    
    print(34 * "-")
    print(pattern.format("currency", "sale", "buy"))
    print(34 * "-")
    for el in sorted_data:
        currency, *_ = el.keys()
        buy = el.get(currency).get("buy")
        sale = el.get(currency).get("sale")
        print(pattern.format(currency, sale, buy))
    print(34 * "-")
    print()

def adapter_data(data: list[dict]):
    
    result = [
        {
            f"{el.get('currency')}": {
                "sale": float(el.get("saleRate")),
                "buy": float(el.get("purchaseRate")),
            }
        }
        for el in data.get("exchangeRate")
        if el.get("currency") in currencies
    ]
    return result

def args_global():
    global currencies
    global n
    parser = argparse.ArgumentParser(
        description="PrivatBank's exchange rate over the past few days"
    )
    parser.add_argument(
        "days", help="days", type=int, choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    )
    parser.add_argument(
        "--currency",
        "-c",
        help="possible currency",
        action="extend",
        default=["EUR", "USD"],
        nargs="+",
        type=str,
        choices=["CHF", "CZK", "GBP", "PLN"],
    )
    args = parser.parse_args()
    currencies = args.currency
    n = args.days

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
                    

async def main():
    args_global()
    now = datetime.now()            # current date and time
    async with aiohttp.ClientSession() as session:
        r=[]
        for i in range(n):            
            date_type_i = now.date() - timedelta(i)
            date_r_i = date_type_i.strftime("%d.%m.%Y")
            r.append(currency_exchange_rate(session, date_r_i))           
        return await asyncio.gather(*r)

if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    data = asyncio.run(main())
    for r in data:
         print(f'date: {r.get("date")}')
         pretty_view(adapter_data(r))

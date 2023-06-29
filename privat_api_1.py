import requests
import argparse
from datetime import date, datetime
from datetime import timedelta


# https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=11
class ApiClient:
    def __init__(self, fetch: requests):
        self.fetch = fetch

    def get_json(self, url):
        response = self.fetch.get(url)
        return response.json()


def pretty_view(data: list[dict]):
    
    pattern = '|{:^10}|{:^10}|{:^10}|'
    print(pattern.format('currency', 'sale', 'buy'))
    print(34*'-')
    for el in data:
        currency, *_ = el.keys()
        buy = el.get(currency).get('buy')
        sale = el.get(currency).get('sale')
        print(pattern.format(currency, sale, buy))


def adapter_data(data: list[dict], currency: list):
    # result = [{f"{el.get('ccy')}": {"buy": float(el.get('buy')), "sale": float(el.get('sale'))}} for el in data]
    result = [{f"{el.get('currency')}": {"sale": float(el.get('saleRate')), "buy": float(el.get('purchaseRate'))}} for el in data.get('exchangeRate') if el.get('currency') in currency]
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PrivatBank's exchange rate over the past few days")
    parser.add_argument("days", help="days",
                    type=int, choices=[1,2,3,4,5,6,7,8,9,10])
    parser.add_argument("--currency", "-c", help = "possible currency", action='extend', default=['EUR', 'USD'], nargs="+", type=str, choices=['CHF', 'CZK', 'GBP', 'PLN'])
    args = parser.parse_args()
    now = datetime.now() # current date and time
    # date_in = input('input date, format = 24.05.2023 \n')
    # date_1 = '01.06.2023'
    # date_type = datetime.strptime(date_1, '%d.%m.%Y')
    # date_r = date_type.strftime('%d.%m.%Y')
    print(args.currency)
    
    n = args.days
    client = ApiClient(requests)
    for i in range(n):
        # date_type_i = date_type - timedelta(i)
        date_type_i = now.date() - timedelta(i)
        date_r_i = date_type_i.strftime('%d.%m.%Y')
        
        data = client.get_json(
            # "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=11"
        "https://api.privatbank.ua/p24api/exchange_rates?json&date="+date_r_i
        )

        print(f'date: {date_r_i}')
        pretty_view(adapter_data(data, args.currency))
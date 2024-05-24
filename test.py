import requests

def RubToTon(rub_amount):
    response = requests.get('https://api.exchangerate-api.com/v4/latest/RUB')
    data = response.json()
    usd_price = 1 / data['rates']['USD']
    response = requests.get(f'https://api.coingecko.com/api/v3/coins/the-open-network?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false')
    data = response.json()
    ton_price_usd = data['market_data']['current_price']['usd']
    ton_price_rub = ton_price_usd * usd_price
    ton_amount = rub_amount / ton_price_rub
    return ton_amount

# Пример использования
rub_amount = 1
ton_amount = RubToTon(rub_amount)
print(f'{rub_amount} RUB is equal to {ton_amount:.8f} TONCOIN(s)')
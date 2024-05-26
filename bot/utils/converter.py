import requests

async def RubToTon(rub_amount):
    response = requests.get('https://api.exchangerate-api.com/v4/latest/RUB')
    data = response.json()
    usd_price = 1 / data['rates']['USD']
    response = requests.get(f'https://api.coingecko.com/api/v3/coins/the-open-network?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false')
    data = response.json()
    ton_price_usd = data['market_data']['current_price']['usd']
    ton_price_rub = ton_price_usd * usd_price
    ton_amount = rub_amount / ton_price_rub
    return ton_amount

async def RubToScale(rub_amount):
    response = requests.get('https://api.exchangerate-api.com/v4/latest/RUB')
    data = response.json()
    usd_price = 1 / data['rates']['USD']
    response = requests.get(f'https://api.coingecko.com/api/v3/coins/scale-network?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false')
    if response.status_code == 200:
        data = response.json()
        scale_price_usd = data['market_data']['current_price']['usd']
        scale_price_rub = scale_price_usd * usd_price
        scale_amount = rub_amount / scale_price_rub
        return scale_amount
    else:
        raise Exception(f'Error {response.status_code}: {response.text}')

async def RubToHedge(rub_amount):
    response = requests.get('https://api.exchangerate-api.com/v4/latest/RUB')
    data = response.json()
    usd_price = 1 / data['rates']['USD']
    response = requests.get(f'https://api.coingecko.com/api/v3/coins/hedge?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false')
    data = response.json()
    hedge_price_usd = data['market_data']['current_price']['usd']
    hedge_price_rub = hedge_price_usd * usd_price
    hedge_amount = rub_amount / hedge_price_rub
    return hedge_amount

async def RubToAmbr(rub_amount):
    response = requests.get('https://api.exchangerate-api.com/v4/latest/RUB')
    data = response.json()
    usd_price = 1 / data['rates']['USD']
    response = requests.get(f'https://api.coingecko.com/api/v3/coins/ambrosus?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false')
    data = response.json()
    ambr_price_usd = data['market_data']['current_price']['usd']
    ambr_price_rub = ambr_price_usd * usd_price
    ambr_amount = rub_amount / ambr_price_rub
    return ambr_amount

async def RubToTake(rub_amount):
    response = requests.get('https://api.exchangerate-api.com/v4/latest/RUB')
    data = response.json()
    usd_price = 1 / data['rates']['USD']
    response = requests.get(f'https://api.coingecko.com/api/v3/coins/take-protocol?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false')
    data = response.json()
    take_price_usd = data['market_data']['current_price']['usd']
    take_price_rub = take_price_usd * usd_price
    take_amount = rub_amount / take_price_rub
    return take_amount

async def RubToTnx(rub_amount):
    response = requests.get('https://api.exchangerate-api.com/v4/latest/RUB')
    data = response.json()
    usd_price = 1 / data['rates']['USD']
    response = requests.get(f'https://api.coingecko.com/api/v3/coins/toncoin?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false')
    data = response.json()
    tnx_price_usd = data['market_data']['current_price']['usd']
    tnx_price_rub = tnx_price_usd * usd_price
    tnx_amount = rub_amount / tnx_price_rub
    return tnx_amount

async def RubToBolt(rub_amount):
    response = requests.get('https://api.exchangerate-api.com/v4/latest/RUB')
    data = response.json()
    usd_price = 1 / data['rates']['USD']
    response = requests.get(f'https://api.coingecko.com/api/v3/coins/bolt?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false')
    data = response.json()
    bolt_price_usd = data['market_data']['current_price']['usd']
    bolt_price_rub = bolt_price_usd * usd_price
    bolt_amount = rub_amount / bolt_price_rub
    return bolt_amount

async def RubToGrbs(rub_amount):
    response = requests.get('https://api.exchangerate-api.com/v4/latest/RUB')
    data = response.json()
    usd_price = 1 / data['rates']['USD']
    response = requests.get(f'https://api.coingecko.com/api/v3/coins/grin?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false')
    data = response.json()
    grbs_price_usd = data['market_data']['current_price']['usd']
    grbs_price_rub = grbs_price_usd * usd_price
    grbs_amount = rub_amount / grbs_price_rub
    return grbs_amount

async def RubToJusdt(rub_amount):
    response = requests.get('https://api.exchangerate-api.com/v4/latest/RUB')
    data = response.json()
    usd_price = 1 / data['rates']['USD']
    response = requests.get(f'https://api.coingecko.com/api/v3/coins/tether?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false')
    data = response.json()
    jusdt_price_usd = data['market_data']['current_price']['usd']
    jusdt_price_rub = jusdt_price_usd * usd_price
    jusdt_amount = rub_amount / jusdt_price_rub
    return jusdt_amount

class RealTimeCurrencyConverter:
    def __init__(self, url):
        self.url = url
        self.data = requests.get(url).json()

    def get_rate(self, from_currency, to_currency):
        if from_currency != 'USD':
            from_currency_rate = self.data['rates'][from_currency]
            return self.data['rates'][to_currency] / from_currency_rate
        else:
            return self.data['rates'][to_currency]
    
def convert_rub_to_usd(amount_rub):
    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
    data = response.json()
    rate = data["rates"]["RUB"]
    amount_usd = amount_rub / rate
    return amount_usd
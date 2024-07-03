import requests

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
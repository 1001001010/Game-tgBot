import requests

def convert_rub_to_usd(amount_rub):
    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
    data = response.json()
    rate = data["rates"]["RUB"]
    amount_usd = amount_rub / rate
    return amount_usd

# Example usage:
amount_rub = 1
amount_usd = convert_rub_to_usd(amount_rub)
print(f"{amount_rub} RUB is equal to {amount_usd} USDT")
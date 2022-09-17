import decimal
import requests
from core import settings


def receive_payment(data):
    ENDPOINT = 'https://payhubghana.io/api/v1.0/debit_mobile_account/'
    headers = {
        "Authorization": f"Token {settings.PAYHUB_SECRET_TOKEN}",
    }
    response = requests.post(ENDPOINT, data=data, headers=headers)
    response_data = response.json()
    print('From receive_payment', response_data)
    return response_data
 

def make_payment(data):
    ENDPOINT = 'https://payhubghana.io/api/v1.0/credit_mobile_account/'
    headers = {
        "Authorization": f"Token {settings.PAYHUB_SECRET_TOKEN}",
    }
    response = requests.post(ENDPOINT, data=data, headers=headers)
    response_data = response.json()
    print("From make_payment", response_data)
    return response_data


def get_transaction_status(transaction_id):
    ENDPOINT = 'https://payhubghana.io/api/v1.0/transaction_status'
    headers = {
        "Authorization": f"Token {settings.PAYHUB_SECRET_TOKEN}",
    }
    params = {
        "transaction_id": transaction_id,
    }
    response = requests.get(ENDPOINT, params=params, headers=headers)
    print('Raw response from get_transaction_status: ', response)
    response_data = response.json()
    print('From get_transaction_status: ', response_data)
    return response_data


def get_api_wallet_balance():
    ENDPOINT = 'https://payhubghana.io/api/v1.0/wallet_balance'
    headers = {
        "Authorization": f"Token {settings.PAYHUB_SECRET_TOKEN}",
    }
    payload = {
        "wallet_id": settings.PAYHUB_WALLET_ID,
    }
    response = requests.get(ENDPOINT, headers=headers, params=payload)
    try:
        main_balance = response.json()['main_balance']
        main_balance = decimal.Decimal(main_balance)
    except KeyError:
        main_balance = decimal.Decimal(0)
    return main_balance


def get_network_codes():
    ENDPOINT = 'https://payhubghana.io/api/v1.0/network_codes'
    headers = {
        "Authorization": f"Token {settings.PAYHUB_SECRET_TOKEN}",
    }
    response = requests.get(ENDPOINT, headers=headers)
    response_data = response.json()
    return response_data

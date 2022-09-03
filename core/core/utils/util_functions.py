

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
    response_data = response.json()
    print('From get_transaction_status: ', response_data)
    return response_data

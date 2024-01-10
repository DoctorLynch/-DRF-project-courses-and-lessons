from django.conf import settings
import requests

api_key = settings.STRIPE_API_KEY


def create_product(product):
    url = 'https://api.stripe.com/v1/products'
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    params = {
        'name': product,
    }
    response = requests.post(url, headers=headers, params=params)
    return response.json()['id']


def create_price(product, price):
    url = 'https://api.stripe.com/v1/prices'
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    params = {
        'currency': 'RUB',
        'product': create_product(product),
        'unit_amount': price
    }
    response = requests.post(url, headers=headers, params=params)
    return response.json()['id']


def get_payment_link(obj):
    url = 'https://api.stripe.com/v1/checkout/sessions'
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    params = {
        'line_items[0][price]': create_price(obj.title, obj.amount),
        'line_items[0][quantity]': 1,
        'mode': 'payment',
        'success_url': 'https://example.com/success',
    }
    response = requests.post(url, headers=headers, params=params)
    return response.json()
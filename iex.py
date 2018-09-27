import requests
from pprint import pprint

API_BASE_URL = 'https://api.iextrading.com/1.0'

def get_symbol(symbol):
	res = requests.get('{}/stock/{}/quote'.format(API_BASE_URL, symbol))
	if res:
		return res.json()
	else:
		return None

def get_symbol_price(symbol):
	json = get_symbol(symbol)
	if json:
		return json['latestPrice']
	else:
		return None

def get_symbol_price_diff(symbol):
	json = get_symbol(symbol)
	if json:
		return json['latestPrice'] - json['open']
	else:
		return None
import requests

from country_code import states
from metric import get_metric_ids
countries = requests.get('http://localhost:3000/regions/').json()
country_dictionary = {}

for country in countries:
    if country['name'] == 'United States':
        for i in country['children']:
            country_dictionary[i['name']] = i['id']

metric_ids = get_metric_ids()

def post_new_cases(data, key):
    body = {
        'region': country_dictionary[states[key]],
        'metric': metric_ids['new_cases_metric'],
        'date': data['date'],
        'value': data['positiveIncrease'] if data['positiveIncrease'] else 0,
        'rollup': False,
        'source': 'https://covidtracking.com'
    }

    url = 'http://localhost:3000/data'
    requests.post(url, body)


def post_active_cases(data, key):
    body = {
        'region': country_dictionary[states[key]],
        'metric': metric_ids['active_metric'],
        'date': data['date'],
        'value': data['positive'] if data['positive'] else 0,
        'rollup': False,
        'source': 'https://covidtracking.com'
    }

    url = 'http://localhost:3000/data'
    requests.post(url, body)


def post_deaths(data, key):
    body = {
        'region': country_dictionary[states[key]],
        'metric': metric_ids['deaths_metric'],
        'date': data['date'],
        'value': data['death'] if data['death'] else 0,
        'rollup': False,
        'source': 'https://covidtracking.com'
    }

    url = 'http://localhost:3000/data'
    requests.post(url, body)


def post_recovered(data, key):
    body = {
        'region': country_dictionary[states[key]],
        'metric': metric_ids['recovered_metric'],
        'date': data['date'],
        'value': data['recovered'] if data['recovered'] else 0,
        'rollup': False,
        'source': 'https://covidtracking.com'
    }

    url = 'http://localhost:3000/data'
    requests.post(url, body)


def get_most_recent_day():
    for key in states:
        r = requests.get(f'https://covidtracking.com/api/v1/states/{key}/daily.json')
        data = r.json()[0]

        post_new_cases(data, key)
        post_active_cases(data, key)
        post_deaths(data, key)
        post_recovered(data, key)


get_most_recent_day()

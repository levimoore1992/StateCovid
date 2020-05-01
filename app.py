import requests

from country_code import states

countries = requests.get('http://localhost:3000/regions/').json()
country_dictionary = {}

for country in countries:
    if country['name'] == 'United States':
        for i in country['children']:
            country_dictionary[i['name']] = i['id']


def post_new_cases(data, key):
    body = {
        'region': country_dictionary[states[key]],
        'metric': 'b206bb67-a919-4d39-b3db-0a36495aa56f',  # UUID for new cases
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
        'metric': '719f7e60-c1a9-4292-ba37-89a3913cb1ff',  # UUID for new cases
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
        'metric': 'e622f7ff-c716-4152-8edd-a65f5ebe9a2d',  # UUID for new cases
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
        'metric': '409f7d1b-1b5b-442f-8ea2-5439c153a79a',  # UUID for new cases
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

import requests
from metric import get_metric_ids
from country_code import states

response = requests.get('https://covidtracking.com/api/v1/states/daily.json').json()

metric_ids = get_metric_ids()

countries = requests.get('http://localhost:3000/regions/').json()
country_dictionary = {}
url = 'http://localhost:3000/data'

for country in countries:
    if country['name'] == 'United States':
        for i in country['children']:
            country_dictionary[i['name']] = i['id']

for item in response:
    try:
        country_dictionary[states[item['state']]]
    except:
        continue

    try:

        new_cases_body = {
            'region': country_dictionary[states[item['state']]],
            'metric': metric_ids['new_cases_metric'],
            'date': item['date'],
            'value': item['positiveIncrease'] if item['positiveIncrease'] else 0,
            'rollup': False,
            'source': 'https://covidtracking.com'
        }
        requests.post(url, new_cases_body)

    except Exception as e:
        print(f'failed on new cases for {item}')
    try:

        deaths_body = {
            'region': country_dictionary[states[item['state']]],
            'metric': metric_ids['deaths_metric'],
            'date': item['date'],
            'value': item['death'] if item['death'] else 0,
            'rollup': False,
            'source': 'https://covidtracking.com'
        }
        requests.post(url, deaths_body)

    except:
        print(f'failed on deaths for {item}')

    try:
        recovered_body = {
            'region': country_dictionary[states[item['state']]],
            'metric': metric_ids['recovered_metric'],
            'date': item['date'],
            'value': item['recovered'] if item['recovered'] else 0,
            'rollup': False,
            'source': 'https://covidtracking.com'
        }
        requests.post(url, recovered_body)

    except:
        print(f'failed on recoveries for {item}')

    try:
        active_body = {
            'region': country_dictionary[states[item['state']]],
            'metric': metric_ids['active_metric'],
            'date': item['date'],
            'value': item['positive'] if item['positive'] else 0,
            'rollup': False,
            'source': 'https://covidtracking.com'
        }
        requests.post(url, active_body)

    except:
        print(f'failed on active cases for {item}')


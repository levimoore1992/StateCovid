import requests
from metric import get_metric_ids
from country_code import states
from datetime import datetime
response = requests.get('https://covidtracking.com/api/v1/states/daily.json').json()

metric_ids = get_metric_ids()

countries = requests.get('http://localhost:3000/regions/').json()
country_dictionary = {}
url = 'http://localhost:3000/data'

for country in countries:
    if country['name'] == 'United States':
        for i in country['children']:
            country_dictionary[i['name']] = i['id']

for item in response[::]:  # we need to search the list in reverse order so that the time series looks right

    #fix date
    item['date'] = str(item['date'])

    # If the item isnt part of the US states ex american samoa it will just move on to the next one
    try:
        country_dictionary[states[item['state']]]
    except:
        continue
    # since each object has all the data we need we can just search the object once and get all the data into
    # four objects that we'll send
    try:
        new_cases_body = {
            'region': country_dictionary[states[item['state']]],
            'metric': metric_ids['new_cases_metric'],
            'date': round(datetime.strptime(item['date'], '%Y%m%d').timestamp() * 1000),
            'value': item['positiveIncrease'] if item['positiveIncrease'] else 0,
            'rollup': False,
            'source': 'https://covidtracking.com'
        }
        requests.post(url, new_cases_body)
    except Exception as e:
        print(f'The application is fine it just couldnt new cases in the this object {item}')
    try:
        deaths_body = {
            'region': country_dictionary[states[item['state']]],
            'metric': metric_ids['deaths_metric'],
            'date': round(datetime.strptime(item['date'], '%Y%m%d').timestamp() * 1000),
            'value': item['death'] if item['death'] else 0,
            'rollup': False,
            'source': 'https://covidtracking.com'
        }
        requests.post(url, deaths_body)
    except:
        print(f'The application is fine it just couldnt  deaths in the this object {item}')
    try:
        recovered_body = {
            'region': country_dictionary[states[item['state']]],
            'metric': metric_ids['recovered_metric'],
            'date': round(datetime.strptime(item['date'], '%Y%m%d').timestamp() * 1000),
            'value': item['recovered'] if item['recovered'] else 0,
            'rollup': False,
            'source': 'https://covidtracking.com'
        }
        requests.post(url, recovered_body)
    except:
        print(f'The application is fine it just couldnt find recoveries in the this object {item}')
    try:
        active_body = {
            'region': country_dictionary[states[item['state']]],
            'metric': metric_ids['active_metric'],
            'date': round(datetime.strptime(item['date'], '%Y%m%d').timestamp() * 1000),
            'value': item['positive'] if item['positive'] else 0,
            'rollup': False,
            'source': 'https://covidtracking.com'
        }
        requests.post(url, active_body)
    except:
        print(f'The application is fine it just couldnt  active cases in the this object {item}')

import requests


def get_metric_ids():
    metrics = requests.get('http://localhost:3000/metrics/')

    metric_ids = {
        'active_metric': '',
        'deaths_metric': '',
        'recovered_metric': '',
        'new_cases_metric': ''
    }

    for metric in metrics:
        if metric['slug'] == 'new-cases':
            metric_ids['new_cases_metric'] = metric['id']

        if metric['slug'] == 'deaths':
            metric_ids['deaths_metric'] = metric['id']

        if metric['slug'] == 'recoveries':
            metric_ids['recovered_metric'] = metric['id']

        if metric['slug'] == 'active-cases':
            metric_ids['active_metric'] = metric['id']

    return metric_ids
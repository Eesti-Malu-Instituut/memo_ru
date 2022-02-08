from lxml import html

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import yaml

import progressbar
import sys


print(f'Fetching records from {sys.argv[1]} to {sys.argv[2]}')

MAX_RECORD = 3115101
n_from = int(sys.argv[1])
n_to = int(sys.argv[2])
RECORD_NUMBERS = range(n_from, n_to)

with open('labels.yaml', 'r') as labels_file:
    fieldnames = yaml.safe_load(labels_file)

retry_strategy = Retry(
    total=10,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)


for nr in progressbar.progressbar(RECORD_NUMBERS):
    url = f'https://base.memo.ru/person/show/{nr}'
    response = http.get(url)
    tree = html.fromstring(response.content)

    for x_prop in tree.xpath('//tr'):
        x_key = x_prop.xpath('./td/text()')[0]
        if x_key not in fieldnames:
            print(f'New label {x_key}.')
            fieldnames.append(x_key)
            with open('labels.yaml', 'w') as labels_file:
                yaml.dump(fieldnames, labels_file)

from lxml import html, etree

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import csv
import yaml
import json

import progressbar
import os
import sys

# import mysql.connector

# mydb = mysql.connector.connect(
#   host="127.0.0.1",
#   user=sys.argv[1],
#   password=sys.argv[2],
#   database="import"
# )
# mycursor = mydb.cursor()

print(f'Fetching records from {sys.argv[3]} to {sys.argv[4]}')

MAX_RECORD = 3115101
n_from = int(sys.argv[3])
n_to = int(sys.argv[4])
RECORD_NUMBERS = range(n_from, n_to)

with open('labels.yaml', 'r') as labels_file:
    fieldnames = yaml.safe_load(labels_file)

f_name = f'out/{n_from}_{n_to - 1}.csv'

with open(f_name, 'w') as f:
    writer = csv.DictWriter(f, fieldnames)
    writer.writeheader()

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
        print(f'Fetch from {url}')
        response = http.get(url)
        print(f'Response from {url}')
        tree = html.fromstring(response.content)

        node = tree.xpath('//div[@class="cont_l cont_l2"]')[0]
        print({node})
        html_val = etree.tostring(node, pretty_print=True)
        print({html_val})
        with open(f'out/{nr}.html', 'wb') as f2:
            f2.write(html_val)

        sql = "INSERT INTO memo_ru_html (id, html) VALUES (%s, %s)"
        val = (nr, html_val)
        print({val})
        mycursor.execute(sql, val)
        mydb.commit()
        # body > section > div.inner_text > div > div.cont_l.cont_l2 > div.line_t_table
        # <div class="line_t_table">Абдулахатова Кульше Исмагуловна</div>
        person = {
            'ID': nr,
            'Name': tree.xpath('//div[@class="line_t_table"]/text()')[0]
        }

        for x_prop in tree.xpath('//tr'):
            # print(x_prop.xpath('./td/text()'), 'XXX\n')
            texts = x_prop.xpath('./td')
            x_key = texts[0].text
            print({x_key})
            # x_val = ','.join(texts[1:])
            x_val = ','.join(map(lambda x: x.text_content(), texts[1:])).replace('\t','')
            print({x_val})
            person[x_key] = x_val
        writer.writerow(person)

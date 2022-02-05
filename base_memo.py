from email import header
from lxml import html
import requests

import csv
import json

import progressbar
import os
import sys

print(f'Fetching records from {sys.argv[1]} to {sys.argv[2]}')

# RECORD_NUMBERS = range(1, 10)
# RECORD_NUMBERS = range(10, 100)
# RECORD_NUMBERS = range(100, 1000)
# rec = 785
# RECORD_NUMBERS = range(rec, rec+1)
# RECORD_NUMBERS = range(1000, 1100)
# RECORD_NUMBERS = range(1100, 100000)
MAX_RECORD = 3115101
n_from = int(sys.argv[1])
n_to = int(sys.argv[2])
RECORD_NUMBERS = range(n_from, n_to)
# RECORD_NUMBERS = range(1, MAX_RECORD + 1)

fieldnames = ['ID', 'Name', 'Место проживания', 'Адрес', 
    'Год рождения', 'Место рождения', 'Реабилитирован', 'Дата реабилитации', 
    'Национальность', 'Осуждён', 'Дата осуждения',
    'Работа', 'Расстреляна', 'Дата ареста',
    'Умерла в местах заключения', 'Умер в местах заключения', 'Архивное дело',
    'Обвинение', 'Приговор', 'Источник']


nr = 1
persons = []
for nr in progressbar.progressbar(RECORD_NUMBERS):
    url = f'https://base.memo.ru/person/show/{nr}'
    page = requests.get(url)
    tree = html.fromstring(page.content)

    # body > section > div.inner_text > div > div.cont_l.cont_l2 > div.line_t_table
    # <div class="line_t_table">Абдулахатова Кульше Исмагуловна</div>
    person = {
        'ID': nr,
        'Name': tree.xpath('//div[@class="line_t_table"]/text()')[0]
    }

    for x_prop in tree.xpath('//tr'):
        # print(x_prop.xpath('./td/text()'), 'XXX\n')
        [x_key, x_val] = x_prop.xpath('./td/text()')
        person[x_key] = x_val
    persons.append(person)
    # print(json.dumps(person))

f_name = f'out/{n_from}_{n_to - 1}.csv'
while True:
    with open(f_name, 'w') as f:
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        writer.writerows(persons)
    print(f'Fetch {f_name}', os.path.isfile(f_name), os.path.getsize(f_name))
    if os.path.isfile(f_name) and os.path.getsize(f_name) > 0:
        break

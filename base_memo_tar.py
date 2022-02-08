import tarfile
from lxml import html, etree

import csv
import yaml
import json

import progressbar
import os
import sys


tar_fn = sys.argv[1]
print(f'Fetching records from {tar_fn}.')

# Initialize file for CSV out
#
csv_file = open(f'{tar_fn}.csv', 'w')
with open('labels.yaml', 'r') as labels_file:
    fieldnames = yaml.safe_load(labels_file)
writer = csv.DictWriter(csv_file, fieldnames)
writer.writeheader()

# Open archive for reading
#
tar = tarfile.open(tar_fn, "r")
for member in progressbar.progressbar(tar):
    f = tar.extractfile(member)
    if f == None:
        continue
    person_nr = os.path.basename(member.name).split('.')[0]
    tree = html.fromstring(f.read())
    name = tree.xpath('//div[@class="line_t_table"]/text()')[0]
    repressions_x = tree.xpath("//*[@class='victims-list']/ul/li")
    # if len(repressions_x) == 1:
    #     continue
    for rep_ix in range(0, len(repressions_x)):
        has_family = False
        repression_x = repressions_x[rep_ix]
        memo_nr = f'{person_nr}_{rep_ix}'
        person = {
            'ID': memo_nr,
            'Name': name
        }

        for x_prop in repression_x.xpath('.//tr'):
            # print(x_prop.xpath('./td/text()'), 'XXX\n')
            texts = x_prop.xpath('./td')
            x_key = texts[0].text
            # print({x_key})
            # x_val = ','.join(texts[1:])
            x_val = ','\
                .join(map(lambda x: x.text_content(), texts[1:]))\
                .replace('\t','')\
                .replace('показать ещё', '')\
                .replace('\n\n', '\n')
            # print({x_val})
            person[x_key] = x_val
            if x_key == 'Члены семьи':
                has_family = True

        # if not has_family:
        #     continue
        writer.writerow(person)

tar.close()
csv_file.close()

exit(0) 


f_name = f'out/{n_from}_{n_to - 1}.csv'

with open(f_name, 'w') as f:
    writer = csv.DictWriter(f, fieldnames)
    writer.writeheader()


    for nr in progressbar.progressbar(RECORD_NUMBERS):
        url = f'https://base.memo.ru/person/show/{nr}'
        print(f'Fetch from {url}')
        response = http.get(url)
        print(f'Response from {url}')
        tree = html.fromstring(response.content)

        node = tree.xpath('//div[@class="cont_l cont_l2"]')[0]
        print({node})


        # body > section > div.inner_text > div > div.cont_l.cont_l2 > div.line_t_table
        # <div class="line_t_table">Абдулахатова Кульше Исмагуловна</div>
        person = {
            'ID': nr,
            'Name': tree.xpath('//div[@class="line_t_table"]/text()')[0]
        }

        writer.writerow(person)

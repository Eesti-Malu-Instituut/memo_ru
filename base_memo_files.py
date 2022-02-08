from lxml import html, etree
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import sys
import progressbar


print(f'Fetching records from {sys.argv[1]} to {sys.argv[2]}')

MAX_RECORD = 3115101
n_from = int(sys.argv[1])
n_to = int(sys.argv[2])
RECORD_NUMBERS = range(n_to, n_from, -1)

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

    outfile = f'out/{nr}.html'
    try:
        node = tree.xpath('//div[@class="cont_l cont_l2"]')[0]
        html_val = etree.tostring(node, pretty_print=True)
        with open(outfile, 'wb') as f2:
            f2.write(html_val)
    except IndexError:
        print(f'\nfailed {url}')


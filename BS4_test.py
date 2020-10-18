import requests
from bs4 import BeautifulSoup


def test(url):
    req = requests.get(url)

    html = req.text

    soup = BeautifulSoup(html, 'html.parser')

    tbody = soup.select(
        '#kboard-default-list > div.kboard-list > table > tbody > tr > td.kboard-list-title > a')

    for item in tbody:
        print(item.get('href'))

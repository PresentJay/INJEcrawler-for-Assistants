import requests
import time
from bs4 import BeautifulSoup
from multiprocessing import Pool

# 20143174 - PresentJay, INJE Univ.


def test(url, ID_, PW_, target_url_prev, target_url_next):

    login_info = {
        'username-77': ID_,
        'user_password-77': PW_
    }

    # HTTP GET Request : use session object on behalf of requests
    # create session, and maintain it in "with" phrase
    with requests.Session() as s:

        res = s.post(url, data=login_info)

        # raise exceptions if the error occurs
        res.raise_for_status()

        # 200 code : success
        """ if res.status_code != 200:
            raise Exception(
                'could not login. please check your ID or PW again.') """

        # pagenated scraping
        pg_count = 1
        target_list = []
        while(1):
            try:
                if get_content(s, target_url_prev + str(pg_count) + target_url_next, target_list) is False:
                    break
                pg_count += 1

            # session retry when session is aborted with connection error or other reason
            except:
                print('error raised in page', pg_count, 'try to retry . . .')
                res = s.post(url, data=login_info)
                res.raise_for_status()

        for item in target_list:
            print(item)


def get_content(session, url, target_list):
    res = session.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    tmp_list = soup.select(
        '#kboard-default-list > div.kboard-list > table > tbody > tr')

    if tmp_list != None:
        for item in tmp_list:
            tmp_dict = {}

            tmp_dict['uid'] = item.contents[3].contents[1].get('href').split('&uid=')[
                1]
            tmp_dict['title'] = item.contents[3].contents[1].contents[1].contents[0].strip()
            tmp_dict['owner'] = item.contents[5].text
            tmp_dict['date'] = item.contents[7].text

            target_list.append(tmp_dict)

    if soup.select_one('#kboard-default-list > div.kboard-pagination > ul > li.last-page') is None:
        print('paginated scraping done. total =', len(target_list), '\n')
        return False

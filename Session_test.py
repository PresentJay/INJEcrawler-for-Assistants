import requests
from bs4 import BeautifulSoup

# 20143174 - PresentJay, INJE Univ.


def test(url, ID_, PW_, target_url_prev, target_url_next):

    login_info = {
        'username-77': ID_,
        'user_password-77': PW_
    }

    # HTTP GET Request : use session object on behalf of requests
    # create session, and maintain it in "with phrase"
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
                res = s.get(target_url_prev + str(pg_count) + target_url_next)
                soup = BeautifulSoup(res.text, 'html.parser')
                tmp_list = soup.select(
                    '#kboard-default-list > div.kboard-list > table > tbody > tr > td.kboard-list-title > a')

                if tmp_list != None:
                    for item in tmp_list:
                        target_list.append(item.get('href'))
                        print('page', pg_count, 'item', len(
                            target_list), 'is in progress')

                if soup.select_one('#kboard-default-list > div.kboard-pagination > ul > li.last-page') is None:
                    print('paginated scraping done.')
                    break

                pg_count += 1

            # session retry when session is aborted with connection error or other reason
            except:
                print('error raised in page', pg_count, 'try to retry . . .')
                res = s.post(url, data=login_info)
                res.raise_for_status()

        for item in target_list:
            print(item)

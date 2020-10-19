import requests
import time
from bs4 import BeautifulSoup
from multiprocessing import Pool

# 20143174 - PresentJay, INJE Univ.


def test(url, ID_, PW_, target_url_prev, target_url_next, target_subject):

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
            # try:
            if get_content(s, target_url_prev + str(pg_count) + target_url_next, target_list, target_subject) is False:
                break
            pg_count += 1

            # session retry when session is aborted with connection error or other reason
            # except:
            #     print('error raised in page', pg_count, 'try to retry . . .')
            #     res = s.post(url, data=login_info)
            #     res.raise_for_status()

        for item in target_list:
            print(item)


def get_content(session, url, target_list, target_subject):
    res = session.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    tmp_list = soup.select(
        '#kboard-default-list > div.kboard-list > table > tbody > tr')

    if tmp_list != None:
        for item in tmp_list:
            tmp_dict = {}
            title = item.contents[3].contents[1].contents[1].contents[0].strip(
            )

            if target_subject in title:
                tmp_dict['Uid'] = item.contents[3].contents[1].get('href').split('&uid=')[
                    1]
                tmp_dict['Title'] = title
                if target_subject == '설계':
                    tmp_dict['Subject'] = '데이터베이스설계및구현'
                else:
                    tmp_dict['Subject'] = target_subject
                if '#' in title:
                    # 일단 과제 수를 1자리수라고 가정하고 간단하게 코딩
                    tmp_dict['HomeworkNum'] = title.split('#')[1].strip()[0]
                elif '과제' in title:
                    tmp_dict['HomeworkNum'] = title.split('과제')[1].strip()[0]

                tmp_dict['Student'] = item.contents[5].text
                tmp_SN = title.split(tmp_dict['Student'])[0].rstrip()

                tmp_dict['StudentNum'] = tmp_SN[-9:-
                                                1] if tmp_SN[-1] is '_' else tmp_SN[-8:]

                tmp_dict['Date'] = item.contents[7].text

                target_list.append(tmp_dict)
            else:
                continue

    if soup.select_one('#kboard-default-list > div.kboard-pagination > ul > li.last-page') is None:
        print('paginated scraping done. total =', len(target_list), '\n')
        return False

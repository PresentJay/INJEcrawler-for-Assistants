from dotenv import load_dotenv
import os
from Session_test import *

# 20143174 - PresentJay, INJE Univ.


def main():
    # get environment variables
    load_dotenv(verbose=True, encoding='UTF8')

    HOME = os.getenv('HOME')
    TARGET = os.getenv('TARGET')
    PAGE = os.getenv('PAGE')
    CATEGORY = os.getenv('CATEGORY')
    CATEGORY_TARGET = os.getenv('CATEGORY_TARGET')
    MOD = os.getenv('MOD')
    ID = os.getenv('ID')
    PW = os.getenv('PW')

    URL_PREV = HOME + TARGET + PAGE
    URL_NEXT = CATEGORY + CATEGORY_TARGET + MOD

    DOWNLOAD_PREV = os.getenv(
        'HOME') + os.getenv('DOWNLOAD_ACTION') + os.getenv('DOWNLOAD_UID_PREV')
    DOWNLOAD_NEXT = os.getenv('DOWNLOAD_UID_NEXT') + \
        os.getenv('DOWNLOAD_NONCE')

    SUBJECT = os.getenv('SUBJECT')

    with requests.Session() as s:
        login_info = {
            'username-77': ID,
            'user_password-77': PW,
            'form_id': '77',
            '_wpnonce': '866658c8ed',
            '_wp_http_referer': "/login/"
        }
        # try:
        res = s.post(os.getenv('LOGIN_URL'), data=login_info)
        res.raise_for_status()

        searchedList = searchByFullPagination(
            s, URL_PREV, URL_NEXT, SUBJECT)
        UidList = get_uid_list(searchedList)

        pool = Pool(os.cpu_count()*2, )
        for item in searchedList:
            det_url = URL_PREV + str(item['pgNum']) + CATEGORY + CATEGORY_TARGET + os.getenv(
                'DETAIL_MOD') + os.getenv('DOWNLOAD_UID_PREV') + str(item['Uid'])

            down_url = DOWNLOAD_PREV + item['Uid'] + DOWNLOAD_NEXT

            get_download(down_url, s, item, det_url)
            break

        # session retry when session is aborted with connection error or other reason
        # except:
        #            s = get_session(os.getenv('LOGIN_URL'), ID, PW)
     #   print('error raised')


if __name__ == "__main__":
    main()

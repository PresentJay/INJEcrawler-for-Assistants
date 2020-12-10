import requests
import time
from multiprocessing import Pool
from bs4 import BeautifulSoup
from DirectoryManager import *
from load_data import *

# 20143174 - PresentJay, INJE Univ.


# 세션 로그인을 수행하는 funcstion
def get_session(session):
    login_info = {
        'username-77': ID,
        'user_password-77': PW
    }

    # HTTP GET Request : use session object on behalf of requests
    # create session, and maintain it in "with" phrase
    res = session.post(LOGIN_URL, data=login_info)

    # raise exceptions if the error occurs
    res.raise_for_status()

    # 200 code : success
    """ if res.status_code != 200:
            raise Exception(
                'could not login. please check your ID or PW again.') """
    return res


def get_wpnonce():
    req = requests.get("https://cs.inje.ac.kr/login/")
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    _wpnonce = soup.select('#_wpnonce')

    return _wpnonce[0]["value"]

def get_download_nonce(session):
    res = session.get()


# 전체 게시글 page를 순회하며 게시글 정보 list를 반환하는 함수
def searchByFullPagination(session):
    # pagenated scraping
    pg_count = 1
    target_list = []
    startTime = time.time()

    # 게시글 끝에 다다를때까지 pagination을 진행시키며, get_content로 각 게시글의 정보를 긁어옴
    while(1):
        # try:
        if get_content(session, target_list, pg_count) is False:
            break
        print('page' + str(pg_count), 'is done')
        pg_count += 1

    print("--- %s seconds for search pages . . . " %
          (time.time() - startTime))

    return target_list


def get_content(session, target_list, pgNum):
    url = URL_PREV + str(pgNum) + URL_NEXT + MOD
    res = session.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    tmp_list = soup.select(
        '#kboard-default-list > div.kboard-list > table > tbody > tr')

    # 페이지 내 게시글 존재할 때
    if tmp_list != None:
        for item in tmp_list:
            tmp_dict = {}
            title = item.contents[3].contents[1].contents[1].contents[0].strip()

            # select by subject
            if SUBJECT in title:
                tmp_dict['Uid'] = item.contents[3].contents[1].get('href').split('&uid=')[1]
                # tmp_dict['Title'] = title

                # Get Subject Name
                if SUBJECT == '설계':
                    tmp_dict['Subject'] = '데이터베이스설계및구현'
                else:
                    tmp_dict['Subject'] = SUBJECT

                # Get Homework Number
                if '#' in title:
                    # 일단 과제 수를 1자리수라고 가정하고 간단하게 코딩
                    tmp_dict['HomeworkNum'] = title.split('#')[-1].strip().replace('_',"")[0]
                elif '과제' in title:
                    tmp_dict['HomeworkNum'] = title.split('과제')[-1].strip().replace('_',"")[0]

                # Get Student Nmae
                tmp_dict['Student'] = item.contents[5].text

                # Get Student Number
                tmp_SN = title.split(tmp_dict['Student'])[0].rstrip()
                tmp_dict['StudentNum'] = tmp_SN[-9:-1] if tmp_SN[-1] is '_' else tmp_SN[-8:]

                # Get Upload Date
                tmp_dict['Date'] = item.contents[7].text

                # check if it is evaluated
                tmp_dict['Done'] = False

                # set page Number
                tmp_dict['pgNum'] = pgNum

                target_list.append(tmp_dict)
            else:
                continue

    # 마지막 페이지 확인시 종료
    if soup.select_one('#kboard-default-list > div.kboard-pagination > ul > li.last-page') is None:
        print('page',pgNum, '(last) is done.')
        print('paginated scraping done. total =',
              len(target_list), ' . . . \n')
        return False


def get_uid_list(src):
    res = []
    for item in src:
        res.append(item['Uid'])
    return res




def get_download(obj, session):
    
    url =  DOWNLOAD_PREV + obj['Uid'] + DOWNLOAD_NEXT
    referer = URL_PREV + str(obj['pgNum']) + URL_NEXT + DETAIL_MOD + DOWNLOAD_UID_PREV + str(obj['Uid'])

    directory = "downloads\\" + obj["Subject"] + "\\과제" + str(obj["HomeworkNum"])
    filename = str(obj["StudentNum"]) + "_" + obj["Student"] + "_" + obj["Date"].replace('.', '-')

    check_directory(directory)

    # print("--- starts download . . . ")
    try:
        res = session.get(url, headers={'Referer': referer})
        if "Content-Disposition" in res.headers:
            with open(directory + '\\' + filename + "." + res.headers["Content-Disposition"].split(".")[-1].replace('"', ""), "wb") as file:
                file.write(res.content)

    except res.HTTPError as e:
        print(e)

    # print("--- Download done . . .")


def get_detail(url, session):
    res = session.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    tmp_list = soup.select(".elementor-widget-container")
    if tmp_list is not None:
        return tmp_list


def get_infopage(text):
    soup = BeautifulSoup(text, "html.parser")
    tmp_list = soup.select("#um_field_general_user_email > div.um-field-area")
    if tmp_list is not None:
        return tmp_list

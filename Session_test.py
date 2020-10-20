import requests
import time
import os
from bs4 import BeautifulSoup
from multiprocessing import Pool, cpu_count
from urllib import request

# 20143174 - PresentJay, INJE Univ.


def get_session(url, session, ID_, PW_):
    login_info = {
        'username-77': ID_,
        'user_password-77': PW_
    }

    # HTTP GET Request : use session object on behalf of requests
    # create session, and maintain it in "with" phrase
    res = session.post(url, data=login_info)

    # raise exceptions if the error occurs
    res.raise_for_status()

    # 200 code : success
    """ if res.status_code != 200:
            raise Exception(
                'could not login. please check your ID or PW again.') """
    return res


def searchByFullPagination(session, target_url_prev, target_url_next, target_subject):
    # pagenated scraping
    pg_count = 1
    target_list = []
    startTime = time.time()

    while(1):
        # try:
        if get_content(session, target_url_prev + str(pg_count) + target_url_next, target_list, target_subject, pg_count) is False:
            break
        print('page' + str(pg_count), 'is done')
        pg_count += 1

    print("--- %s seconds for search pages . . . " %
          (time.time() - startTime))

    return target_list

    # pool = Pool(processes=cpu_count())
    # print(get_uid_list(target_list))


def get_content(session, url, target_list, target_subject, pgNum):
    res = session.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    tmp_list = soup.select(
        '#kboard-default-list > div.kboard-list > table > tbody > tr')

    # 페이지 내 게시글 존재할 때
    if tmp_list != None:
        for item in tmp_list:
            tmp_dict = {}
            title = item.contents[3].contents[1].contents[1].contents[0].strip(
            )

            # select by subject
            if target_subject in title:
                tmp_dict['Uid'] = item.contents[3].contents[1].get('href').split('&uid=')[
                    1]
                # tmp_dict['Title'] = title

                # Get Subject Name
                if target_subject == '설계':
                    tmp_dict['Subject'] = '데이터베이스설계및구현'
                else:
                    tmp_dict['Subject'] = target_subject

                # Get Homework Number
                if '#' in title:
                    # 일단 과제 수를 1자리수라고 가정하고 간단하게 코딩
                    tmp_dict['HomeworkNum'] = title.split('#')[
                        1].strip()[0]
                elif '과제' in title:
                    tmp_dict['HomeworkNum'] = title.split('과제')[
                        1].strip()[0]

                # Get Student Nmae
                tmp_dict['Student'] = item.contents[5].text

                # Get Student Number
                tmp_SN = title.split(tmp_dict['Student'])[0].rstrip()
                tmp_dict['StudentNum'] = tmp_SN[-9:-
                                                1] if tmp_SN[-1] is '_' else tmp_SN[-8:]

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
        print('paginated scraping done. total =',
              len(target_list), ' . . . \n')
        return False


def get_uid_list(src):
    res = []
    for item in src:
        res.append(item['Uid'])
    return res


def check_directory(dirname):
    current = "."
    for item in dirname.split('\\'):
        current += "\\" + item
        if os.path.exists(current) is False:
            os.mkdir(current)
            print("create directory >", current)


def get_download(url, session, obj, referer):

    directory = obj["Subject"] + "\\과제" + str(obj["HomeworkNum"])
    filename = str(obj["StudentNum"]) + "_" + \
        obj["Student"] + "_" + obj["Date"].replace('.', '-')

    print(directory + "\\" + filename)
    check_directory(directory)

    print("--- starts download . . . ")
    try:
        res = session.get(url, headers={'Referer': referer})
        with open(directory + '\\' + filename + "." + res.headers["Content-Disposition"].split(".")[1].replace('"', ''), "wb") as file:
            file.write(res.content)

    except request.HTTPError as e:
        print(e)

    print("--- Download done . . .")


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

from crawler import *
from itertools import repeat
# from functools import partial

# 20143174 - PresentJay, INJE Univ.


def main():

    with requests.Session() as s:
        login_info = config["login_info"]
        login_info['username-77']= ID
        login_info['user_password-77']= PW
        
        # try:
        res = s.post(os.getenv('LOGIN_URL'), data=login_info)
        res.raise_for_status()

        searchedList = searchByFullPagination(s)
        UidList = get_uid_list(searchedList)

        e_time = time.time()
        
        with Pool(os.cpu_count()) as pool:
            pool.starmap(get_download, zip(searchedList, repeat(s)))
            # pool.map(partial(get_download, session = s), searchedList)
            
        print(time.time()-e_time,"seconds elapsed. . .")
        
        # count = 1
        # for item in searchedList:
        #     det_url = URL_PREV + str(item['pgNum']) + CATEGORY + CATEGORY_TARGET + os.getenv(
        #         'DETAIL_MOD') + os.getenv('DOWNLOAD_UID_PREV') + str(item['Uid'])

        #     down_url = DOWNLOAD_PREV + item['Uid'] + DOWNLOAD_NEXT
        #     print("(" + str(count) + "/" + str(len(searchedList)) + ") download complete /",
        #           time.time() - e_time, "second elapsed :", item['Student'])
        #     get_download(down_url, s, item, det_url)
        #     count += 1
            
        # session retry when session is aborted with connection error or other reason
        """ except:
            s = get_session(os.getenv('LOGIN_URL'), ID, PW)
            print('error raised') """


if __name__ == "__main__":
    main()

from load_data import *
from crawler import *
from itertools import repeat
from DirectoryManager import *
from ExcelAccessment import *
# from functools import partial

# 20143174 - PresentJay, INJE Univ.

def main():

    with requests.Session() as s:
        login_info = config["login_info"]
        login_info['username-77']= ID
        login_info['user_password-77']= PW
        login_info['_wpnonce'] = get_wpnonce()
        
        # try:
        res = s.post(os.getenv('LOGIN_URL'), data=login_info)
        res.raise_for_status()
        
        # stdlist = readExcelData("C:\\Users\\PresentJay\\Desktop\\2020-데이터베이스설계및구현-과제채점\\데이터베이스설계및구현_수강생명단.xlsx")
        # arrangeFiles("데이터베이스설계및구현", stdlist)

        searchedList = searchByFullPagination(s)
        # UidList = get_uid_list(searchedList)
        
        e_time = time.time()
        
        # print("start download", len(searchedList), "files. . .")
        
        
        print("start delete")
        if SUBJECT is "설계":
            subject = "데이터베이스설계및구현"
        else:
            subject = SUBJECT
        remove_list = get_currentFiles(subject)
        
    
        # delete_page(searchedList[0], res)
        
        
        with Pool(os.cpu_count()) as pool:
            pool.starmap(delete_page, zip(searchedList, repeat(s)))
            # pool.map(partial(get_download, session = s), searchedList)
        
        # if target["Student"] in remove_list:
        #     delete_page(target, s)
        # else:
        #     print("error errupt")
        
        # with Pool(os.cpu_count()) as pool:
        #     pool.starmap(get_download, zip(searchedList, repeat(s)))
        #     # pool.map(partial(get_download, session = s), searchedList)
            
        print(time.time()-e_time,"seconds elapsed. . .")
        
        # session retry when session is aborted with connection error or other reason
        """ except:
            s = get_session(os.getenv('LOGIN_URL'), ID, PW)
            print('error raised') """
            
        


if __name__ == "__main__":
    main()

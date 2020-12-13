import os.path
import shutil
from load_data import *
from ExcelAccessment import *

""" DirectoryManager.py """
# Directory를 이용한 Function을 정의합니다.


""" Function getFiles """
# 특정 Directory의 File목록을 반환합니다.
# config의 IGNOREFILE_DEFAULT 목록을 무시합니다.
# (1) 첫 번째 매개변수로 기준 Directory를 결정합니다. (기본값 : 현재 폴더)
# (2) 두 번째 매개변수로 확장자를 결정합니다. (기본값 : 모든 파일)
# (3) 세 번째 매개변수로 절대경로/상대경로를 결정합니다. (기본값 : 절대경로)


def getFiles(_dir=os.getcwd(), extension='*', absolute=True):
    files = []
    for _file in os.listdir(_dir):  # (1)
        # 프로젝트 기본파일들을 제외합니다 (load_data.py에 정의)
        ignore = config['IGNOREFILE_DEFAULT']
        unzip__projectfiles(ignore)

        if _file in ignore:
            continue  # (2)
        if extension != '*' and _file.split('.')[1] != extension:
            continue  # (3)
        if absolute:
            _file = os.path.join(_dir, _file)
        files.append(_file)
    return files


def check_directory(dirname):
    current = "."
    for item in dirname.split('\\'):
        current += "\\" + item
        if (os.path.exists(current) is False):
            os.mkdir(current)
            print("create directory > {}".format(current))
            


def arrangeFiles(sbj, students):
    basedir = "downloads\\" + sbj + "\\"
    
    for _ in range(1,10):
        middir = "과제{}".format(_)
        check_directory(basedir + middir)
        for __ in range(0, 5):
            check_directory(basedir + middir + "\\{}점".format(__))
    
    for _ in students:
        for work in range(1, 10):
            workdir = basedir + "과제{}".format(work)
            enddir = workdir + "\\끝"
            for file in os.listdir(enddir):
                if file.split("_")[0] == _["stdnum"]:
                    newdir ="{}\\{}점".format(workdir, _["works"][work-1])
                    shutil.move(enddir+"\\" +file, newdir)
                    print("change>>",enddir+file, "to", newdir)
            shutil.rmtree(enddir)
            

def get_currentFiles(obj):
    basedir = os.path.join("downloads", obj, "과제")
    
    res = []
    
    for _ in range(1, 10):
        _dir = basedir + str(_)
        if os.path.exists(_dir):    
            tmp = {
                "subject" : obj,
                "worknum" : _,
                "dir" : _dir,
                "member": []
            }
            if obj == "데이터베이스설계및구현":
                for __ in range(1, 5):
                    _score = "{}점".format(__)
                    _scorepath = os.path.join(tmp["dir"], _score)
                    if os.path.exists(_scorepath):
                        for file in os.listdir(_scorepath):
                            tmp["member"].append(file.split("_")[1])
            elif obj == "데이터구조":
                tmp["member"] = []
                for file in os.listdir(tmp["dir"]):
                    tmp["member"].append(file.split("_")[1])
            res.append(tmp)
        else:
            continue
    return res

# def get_currentFiles(obj, homeworknum):
#     basedir = os.path.join("downloads", obj, "과제{}".format(homeworknum))
#     res = []
#     if os.path.exists(basedir):    
#         if obj == "데이터베이스설계및구현":
#             for __ in range(1, 5):
#                 _score = "{}점".format(__)
#                 _scorepath = os.path.join(basedir, _score)
#                 if os.path.exists(_scorepath):
#                     for file in os.listdir(_scorepath):
#                         res.append(file.split("_")[1])
#         elif obj == "데이터구조":
#             tmp["member"] = []
#             for file in os.listdir(basedir):
#                 res.append(file.split("_")[1])
#     return res
            
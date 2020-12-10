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
        if os.path.exists(current) is False:
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
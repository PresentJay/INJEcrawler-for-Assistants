import openpyxl as xl
from CommandDecorator import *

def readExcelData(_dir):
    book = xl.load_workbook(_dir)
    
    sheet = book['Sheet1']
    
    students= []
    
    for _ in range(3, 55):
        works = []
        for __ in sheet["F{}:N{}".format(_,_)]:
            for cell in __:
                works.append(cell.value)
        student = {
            "name" : sheet["D{}".format(_)].value,
            "stdnum" : sheet["C{}".format(_)].value,
            "works" : works
        }
        students.append(student)
        
    print(_dir," sheet is read")
    
    return students


def getFilename(studentInfo):
    return (studentInfo["stdnum"] + "_" + studentInfo["name"])
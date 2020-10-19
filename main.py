from dotenv import load_dotenv
import os
from Session_test import *

# 20143174 - PresentJay, INJE Univ.


def main():
    # get environment variables
    load_dotenv(verbose=True)

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

    test(os.getenv('LOGIN_URL'), ID, PW, URL_PREV, URL_NEXT)
    # test(, ID, PW)


if __name__ == "__main__":
    main()

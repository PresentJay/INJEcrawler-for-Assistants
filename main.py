from dotenv import load_dotenv
import os
from Requests_test import *

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

    test(HOME + TARGET + PAGE + CATEGORY + CATEGORY_TARGET + MOD)


if __name__ == "__main__":
    main()

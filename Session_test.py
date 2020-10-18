import requests

# 20143174 - PresentJay, INJE Univ.


def test(url, ID_, PW_):

    login_info = {
        'username-77': ID_,
        'user_password-77': PW_
    }

    # HTTP GET Request : use session object on behalf of requests
    # create session, and maintain it in "with phrase"
    with requests.Session() as s:

        login_req = s.post(url, data=login_info)

        print(login_req.status_code)

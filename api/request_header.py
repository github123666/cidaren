import requests

from decryptencrypt.encrypt_md5 import encrypt_md5

Token = ''
user_age = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309080f) XWEB/8501 Flue"
headers = {"Host": "app.vocabgo.com",
           "Accept": "application/json, text/plain, */*",
           "Abc": encrypt_md5(user_age),
           "Authorization-V": "cfcd208495d565ef66e7dff9f98764da",
           "X-Requested-With": "XMLHttpRequest",
           "User-Agent": user_age,
           "Accept-Language": "*",
           "Sec-Fetch-Site": "same-origin",
           "Sec-Fetch-Mode": "cors",
           "Sec-Fetch-Dest": "empty",
           "Referer": "https://app.vocabgo.com/student/",
           "Accept-Encoding": "gzip, deflate, br"
           }

rqs_session = rqs2_session = rqs3_session = ''


def set_token(token):
    global Token
    Token = token
    global rqs_session, rqs2_session, rqs3_session
    rqs_session = requests.session()
    rqs_session.headers = headers
    rqs_session.headers.update({'Usertoken': Token})
    # submit request header
    rqs2_session = requests.session()
    rqs2_session.headers = headers.copy()
    rqs2_session.headers.update(
        {"Authorization-V": "c4ca4238a0b923820dcc509a6f75849b", 'Usertoken': Token, "Origin": "https://app.vocabgo.com",
         "Content-Type": "application/json", "Content-Length": "393"})
    rqs3_session = requests.session()
    rqs3_session.headers = headers.copy()
    rqs3_session.headers.update({"Origin": "https://app.vocabgo.com", 'Usertoken': Token,
                                 "Content-Type": "application/json", "Content-Length": "460"})

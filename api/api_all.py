import json

import requests

from decryptencrypt.createSign import create_sign
from decryptencrypt.debase64 import debase64
from log.log import Log
from util.create_timestamp import create_timestamp

# create logger
api = Log('api')
# init request
basic_url = 'https://app.vocabgo.com/student/api/Student/'
rqs_session = requests.session()
rqs_session.headers = {"Host": "app.vocabgo.com",
                       "Accept": "application/json, text/plain, */*",
                       "Abc": "0b1f3963e0b8556",
                       "Authorization-V": "cfcd208495d565efa",
                       "X-Requested-With": "XMLHttpRequest",
                       "Usertoken": "9cab7a572a85aad69d6",
                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309080f) XWEB/8501 Flue",
                       "Accept-Language": "*",
                       "Sec-Fetch-Site": "same-origin",
                       "Sec-Fetch-Mode": "cors",
                       "Sec-Fetch-Dest": "empty",
                       "Referer": "https://app.vocabgo.com/student/",
                       "Accept-Encoding": "gzip, deflate, br"
                       }
# submit result
headers = {"Host": "app.vocabgo.com",
           "Cookie": "_gid=GA1.2.1973191695.1702951694; _ga_4WFCFXM0S9=GS1.1.1702951690.1.1.1702952064.57.0.0; _ga=GA1.1.1189001824.1702951691",
           "Content-Length": "393",
           "Accept": "application/json, text/plain, */*",
           "Abc": "0b1f3963e0b855647",
           "Authorization-V": "c4ca4238a",
           "X-Requested-With": "XMLHttpRequest",
           "Usertoken": "9cab7a572a85a",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309080f) XWEB/8501 Flue",
           "Content-Type": "application/json",
           "Accept-Language": "*",
           "Origin": "https://app.vocabgo.com",
           "Sec-Fetch-Site": "same-origin",
           "Sec-Fetch-Mode": "cors",
           "Sec-Fetch-Dest": "empty",
           "Referer": "https://app.vocabgo.com/student/",
           "Accept-Encoding": "gzip, deflate, br"
           }


# response is 200
def handle_response(response: requests.models.Response):
    if response.ok:
        api.logger.info(f"请求成功{response.content}")
    else:
        api.logger.info(f"请求有问题{response.content}退出程序")
        exit(-1)


# start
def get_exam(public_info):
    api.logger.info("获取第一个topic_code")
    url = f'StudyTask/StartAnswer?task_id=91158510&task_type=3&course_id=CET4_pre&opt_img_w=' \
          f'1704&opt_font_size=94&opt_font_c=%23000000&it_img_w=2002&it_font_size=106&timestamp={create_timestamp()}&version=2.6.1.231204&app_type=1'
    rsp = rqs_session.get(basic_url + url)
    # check response is success
    handle_response(rsp)
    # handle encrypt
    print(rsp.json())
    public_info.exam = debase64(rsp.json())
    api.logger.info("写入成功")


def next_exam(public_info):
    api.logger.info("获取下一题")
    url = 'StudyTask/SubmitAnswerAndSave'
    timestamp = create_timestamp()
    topic_code = public_info.topic_code
    # topic_code = "kld4e4psl9LTmVKRV3l8jGyYoqrHl2dnWmJbqJrM2aKV1cyoolmOaGZhaGdqZL2TkVzAkmJoZGllY2+SanBnbG5uZmmVnGKPvJWWkWOTaGFpb2JvbZeXamidYWljcWlqZ3CXaWdiaWlyam6XnGxrjZNlZJQ="
    sign = f"timestamp={timestamp}&topic_code={topic_code}&version=2.6.1.231204ajfajfamsnfaflfasakljdlalkflak"
    data = {
        "time_spent": 3417, "opt_img_w": 1704, "opt_font_size": 94, "opt_font_c": "#000000", "it_img_w": 2002,
        "it_font_size": 106,
        "topic_code": topic_code,
        "timestamp": timestamp, "version": "2.6.1.231204", "sign": sign,
        "app_type": 1}
    rsp = requests.post(basic_url + url, headers=headers, data=json.dumps(data))
    print(rsp.text)
    public_info.exam = debase64(rsp.json())


# query word
def query_word(public_info, word):
    url = f'Course/StudyWordInfo?course_id=CET4_pre&list_id=CET4_pre_01&word={word}&timestamp={create_timestamp()}&version=2.6.1.231204&app_type=1'
    rsp = rqs_session.get(basic_url + url)
    # check request is success
    handle_response(rsp)
    # handle encrypt
    public_info.word_query_result = debase64(rsp.json())
    api.logger.info("查询完成")


# submit word
def submit_result(public_info, option: int):
    api.logger.info("开始提交")
    timestamp = create_timestamp()
    topic_code = public_info.topic_code
    sign = create_sign(
        f"answer=3&timestamp={timestamp}&topic_code={topic_code}&version=2.6.1.231204ajfajfamsnfaflfasakljdlalkflak")
    print(sign)
    url = "StudyTask/VerifyAnswer"
    data = {"answer": option,
            "topic_code": topic_code,
            "timestamp": timestamp, "version": "2.6.1.231204", "sign": sign,
            "app_type": 1}
    rsp = requests.post(basic_url + url, headers=headers, data=json.dumps(data))
    api.logger.info("提交返回结果")
    print(rsp.json())
    public_info.topic_code = debase64(rsp.json())['topic_code']


if __name__ == '__main__':
    a = {}
    query_word(a,"desire")
    # test sign
    # sign_source = f"answer=2&timestamp=1702802043947&topic_code=kld4e4psl9LTmVKRV3l8jGyYoqrHl2doWmJbnKTX0Zegg49qZWOaa2phkWmVZL2+YGGRZmJob2hramiUaGlscWZsYpDCkGdnjZdyYG6XbGtrbm5ka46aZWKaaWluaGRqZXGWcW5ucW9lZmGVwQ==&version=2.6.1.231204ajfajfamsnfaflfasakljdlalkflak"
    # print(create_sign(sign_source))
    # submit_result()
# topic_code()

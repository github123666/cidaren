import json

import api.request_header as requests
from decryptencrypt.debase64 import debase64
from decryptencrypt.encrypt_md5 import encrypt_md5
from log.log import Log
from util.create_timestamp import create_timestamp

# create logger
api = Log('api')

basic_url = 'https://app.vocabgo.com/student/api/Student/'


# response is 200
def handle_response(response):
    rsp_json = response.json()
    code = rsp_json['code']
    if code == 1:
        api.logger.info(f"请求成功{response.content}")
    # complete exam
    elif code == 20001 and rsp_json['data']:
        pass
    else:
        api.logger.info(f"请求有问题{response.text}退出程序")
        exit(-1)





# select all word exam
def select_all_word(key, word_list, task_id: int) -> None:
    api.logger.info("勾选全部单词并提交")
    timestamp = create_timestamp()
    url = 'StudyTask/SubmitChoseWord'
    word_map = json.dumps({key: word_list}, separators=(',', ':'))
    source_str = f'chose_err_item=2&task_id={task_id}&timestamp={timestamp}&version=2.6.1.231204&word_map={word_map}ajfajfamsnfaflfasakljdlalkflak'
    sign = encrypt_md5(source_str)
    data = {"task_id": task_id, "word_map": {
        key: word_list}, "chose_err_item": 2,
            "timestamp": timestamp, "version": "2.6.1.231204", "sign": sign,
            "app_type": 1}
    rsp = requests.rqs3_session.post(basic_url + url, data=json.dumps(data))
    # check request is success
    handle_response(rsp)


# start
def get_exam(public_info):
    api.logger.info("获取第一个题topic_code")
    url = f'StudyTask/StartAnswer?task_id={public_info.task_id}&task_type=3&course_id={public_info.course_id}&opt_img_w=' \
          f'1704&opt_font_size=94&opt_font_c=%23000000&it_img_w=2002&it_font_size=106&timestamp={create_timestamp()}&version=2.6.1.231204&app_type=1'
    rsp = requests.rqs_session.get(basic_url + url)
    # check response is success
    handle_response(rsp)
    #  decrypt response
    public_info.exam = debase64(rsp.json())
    api.logger.info("写入成功")


# next exam
def next_exam(public_info):
    api.logger.info("获取下一题")
    url = 'StudyTask/SubmitAnswerAndSave'
    timestamp = create_timestamp()
    topic_code = public_info.topic_code
    # sign 是乱写的后台好像不会验证
    sign = f"timestamp={timestamp}&topic_code={topic_code}&version=2.6.1.231204ajfajfamsnfaflfasakljdlalkflak"
    data = {
        "time_spent": 3417, "opt_img_w": 1704, "opt_font_size": 94, "opt_font_c": "#000000", "it_img_w": 2002,
        "it_font_size": 106,
        "topic_code": topic_code,
        "timestamp": timestamp, "version": "2.6.1.231204", "sign": sign,
        "app_type": 1}
    rsp = requests.rqs2_session.post(basic_url + url, data=json.dumps(data))
    # check request is success
    handle_response(rsp)
    if rsp.json()['msg'] == '需要选词！':
        public_info.exam = 'complete'
    # decrypt response
    else:
        public_info.exam = debase64(rsp.json())


# query word
def query_word(public_info, word):
    url = f'Course/StudyWordInfo?course_id={public_info.course_id}&list_id={public_info.now_unit}&word={word}&timestamp={create_timestamp()}&version=2.6.1.231204&app_type=1'
    rsp = requests.rqs_session.get(basic_url + url)
    # check request is success
    handle_response(rsp)
    # decrypt  response
    public_info.word_query_result = debase64(rsp.json())
    api.logger.info("查询单词成功")


# submit word
def submit_result(public_info, option):
    api.logger.info("开始提交答案")
    timestamp = create_timestamp()
    topic_code = public_info.topic_code
    sign = encrypt_md5(
        f"answer={option}&timestamp={timestamp}&topic_code={topic_code}&version=2.6.1.231204ajfajfamsnfaflfasakljdlalkflak")
    url = "StudyTask/VerifyAnswer"
    data = {"answer": option,
            "topic_code": topic_code,
            "timestamp": timestamp, "version": "2.6.1.231204", "sign": sign,
            "app_type": 1}
    print(data)
    rsp = requests.rqs2_session.post(basic_url + url, data=json.dumps(data))
    # check request is success
    handle_response(rsp)
    api.logger.info("提取下一题的请求参数")
    # next exam topic_code
    public_info.topic_code = debase64(rsp.json())['topic_code']


if __name__ == '__main__':
    pass

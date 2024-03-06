import json
import random
import time
from functools import wraps

import api.request_header as requests
from decryptencrypt.debase64 import debase64
from decryptencrypt.encrypt_md5 import encrypt_md5
from log.log import Log
from publicInfo.publicInfo import PublicInfo
from util.basic_utll import create_timestamp

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
    elif code == 20001 and rsp_json['data'] or code == 20004:
        pass
    elif code == 0 and rsp_json['msg'] == '加载单词卡片失败，请重新加载':
        api.logger.error("查找不到单词(第三方库转不了时态),请手动答题")
        exit('请手动答题,已退出')
    else:
        api.logger.info(f"请求有问题{response.text}退出程序", stack_info=True)
        exit(-1)




# select all word
def select_all_word(word_info, task_id: int, ) -> None:
    api.logger.info("勾选全部单词并提交")
    timestamp = create_timestamp()
    url = f'{PublicInfo.task_type}/SubmitChoseWord'
    # 取消键值对的空格(紧密排版)
    word_map = json.dumps(word_info, separators=(',', ':'))
    source_str = f'chose_err_item=2&task_id={task_id}&timestamp={timestamp}&version=2.6.1.231204&word_map={word_map}ajfajfamsnfaflfasakljdlalkflak'
    sign = encrypt_md5(source_str)
    data = {"task_id": task_id, "word_map": word_info, "chose_err_item": 2,
            "timestamp": timestamp, "version": "2.6.1.231204", "sign": sign,
            "app_type": 1}
    rsp = requests.rqs3_session.post(basic_url + url, data=json.dumps(data))
    # check request is success
    handle_response(rsp)


# class task
# get all the  tasks for the class
def get_class_task(public_info, page_count: int):
    """
    :param public_info:
    :param page_count:  第几页的数据
    :return:
    """
    api.logger.info('获取10个班级任务')
    url = 'ClassTask/PageTask'
    timestamp = create_timestamp()
    sign = f"page_count={page_count}&page_size=10&search_type=0&timestamp={timestamp}&version=2.6.1.240122ajfajfamsnfaflfasakljdlalkflak"
    data = {
        'search_type': '0',
        'page_count': page_count,
        'page_size': 10,
        'timestamp': timestamp,
        "version": "2.6.1.231204",
        "sign": encrypt_md5(sign),
        "app_type": 1
    }
    rsp = requests.class_task_request.post(url=basic_url + url, json=data)
    # check response is success
    handle_response(rsp)
    rsp_dict = rsp.json()
    # sava public_info
    public_info.class_task.append(rsp_dict['data'])
    # number of task
    public_info.task_total_count = rsp_dict['data']['total']


# # start

def get_exam(public_info):
    api.logger.info("获取第一题")
    url = f'{PublicInfo.task_type}/StartAnswer'
    params = {'task_id': public_info.task_id or -1, 'task_type': PublicInfo.task_type_int,
              'opt_img_w': '684',
              'opt_font_size': '37', 'opt_font_c': '%23000000', 'it_img_w': '804', 'it_font_size': '42',
              'timestamp': create_timestamp(), 'version': '2.6.1.240122', 'app_type': '1'}
    if PublicInfo.task_type_int == 2:
        params.update({'release_id': public_info.release_id})
    else:
        params.update({'course_id': public_info.course_id})
    rsp = requests.class_task_request.get(url=basic_url + url, params=params)
    # check response is success
    handle_response(rsp)
    #  decrypt response
    public_info.exam = debase64(rsp.json())
    api.logger.info("写入成功")


# next exam
def next_exam(public_info):
    api.logger.info("获取下一题")
    url = f'{PublicInfo.task_type}/SubmitAnswerAndSave'
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
    if rsp.json()['msg'] == '任务已完成！' or rsp.json()['msg'] == '需要选词！':
        public_info.exam = 'complete'
    # decrypt response
    else:
        public_info.exam = debase64(rsp.json())


def check_is_self_built(func):
    @wraps(func)
    def is_self_built(public_info, word):
        if public_info.is_self_built:
            # get word index in the word_list
            word_index = public_info.word_list.index(word)
            # get word in the unit
            public_info.now_unit = public_info.get_book_words_data[word_index]["list_id"]
        return func(public_info, word)

    return is_self_built


# query word
@check_is_self_built
def query_word(public_info, word):
    time.sleep(random.randint(0, 2))
    api.logger.info(f"查询单词{word}")
    # query word in the unit
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
    url = f"{PublicInfo.task_type}/VerifyAnswer"
    data = {"answer": option,
            "topic_code": topic_code,
            "timestamp": timestamp, "version": "2.6.1.231204", "sign": sign,
            "app_type": 1}
    rsp = requests.rqs2_session.post(basic_url + url, data=json.dumps(data))
    # check request is success
    handle_response(rsp)
    api.logger.info("提取下一题的请求参数")
    # next exam topic_code
    public_info.topic_code = debase64(rsp.json())['topic_code']


if __name__ == '__main__':
    pass

import api.request_header as requests
from log.log import Log
from util.basic_utll import create_timestamp


# init log
basic_api = Log("basic_api")
basic_url = 'https://app.vocabgo.com/student/api/Student/'


# response is 200
def handle_response(response):
    if response.json()['code'] == 1:
        basic_api.logger.info(f"请求成功{response.content}")
    else:
        basic_api.logger.info(f"请求有问题{response.text}退出程序")
        exit(-1)


def get_select_course(public_info):
    url = 'Main?timestamp=1704182548197&version=2.6.1.231204&app_type=1'
    rsp = requests.rqs_session.get(basic_url + url)
    # check request is success
    handle_response(rsp)
    # course id
    public_info.course_id = rsp.json()['data']['user_info']['course_id']


def get_all_unit(public_info):
    timestamp = create_timestamp()
    url = f'StudyTask/List?course_id={public_info.course_id}&timestamp={timestamp}&version=2.6.1.231204&app_type=1'
    rsp = requests.rqs_session.get(basic_url + url)
    # check response is success
    handle_response(rsp)
    public_info.all_unit = rsp.json()['data']


def get_unit_id(public_info):
    timestamp = create_timestamp()
    url = f'StudyTask/Info?task_id=-1&course_id={public_info.course_id}&list_id={public_info.now_unit}&timestamp={timestamp}&version=2.6.1.231204&app_type=1'
    rsp = requests.rqs_session.get(basic_url + url)
    # check request is success
    handle_response(rsp)
    rsp_json = rsp.json()
    public_info.task_id = rsp_json['data']['task_id']
    public_info.get_word_list_result = rsp_json


def get_all_task(public_info):
    url = '/Student/ClassTask/PageTask'
    basic_api.logger.info('获取所有班级任务')



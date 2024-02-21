import os

import api.request_header as requests
from answer_questions.answer_questions import *
from api.basic_api import get_all_unit, get_unit_id, get_select_course
from api.login import verify_token, get_token
from api.main_api import get_exam, select_all_word, get_class_task, get_class_exam
from log.log import Log
from publicInfo.publicInfo import PublicInfo
from util.basic_utll import filler_not_complete_unit, filter_expire_task
from util.handle_word_list import handle_word_result


def complete_test(task_info: dict):
    """
    完成班级任务的测试
    :param task_info: 测试任务信息
    :return: None
    """

    task_name = task_info['task_name']
    public_info.course_id = task_info['course_id']
    main.logger.info(f'完成{task_name}')
    # get unit id
    main.logger.info('用course_id匹配单元list_id')
    # get all the units of the book
    main.logger.info('获取该书的所有单元')
    get_all_unit(public_info)
    for unit in public_info.all_unit['task_list']:
        if unit['task_name'] == task_name:
            public_info.now_unit = unit['list_id']
    unit_progress = task_info['progress']
    # myself exam task_id
    if task_info['task_type'] == 1:
        main.logger.info('完成班级任务的自学任务')
        complete_practice(public_info.now_unit, unit_progress, task_info['task_id'])
    else:
        get_unit_id(public_info)  # return now unit all word
        # extract return word
        handle_word_result(public_info)
        public_info.task_id = task_info['task_id']
        # get first exam
        public_info.release_id = task_info['release_id']
        get_class_exam(public_info)
        public_info.topic_code = public_info.exam['topic_code']
        main.logger.info("开始答题")
        option = 0
        while True:
            main.logger.info("获取题目类型")
            if public_info.exam == 'complete':
                # unit complete skip next unit
                break
            mode = public_info.exam['topic_mode']
            main.logger.info(f'题目类型{mode}')
            if mode == 17 or mode == 18:
                option = mean_to_word(public_info)
            elif mode == 15 or mode == 16 or mode == 21 or mode == 22:
                option = word_form_mean(public_info)
            elif mode == 11 or mode == 22:
                option = word_form_mean(public_info)
            elif mode == 32:
                option = select_word(public_info)
            elif mode == 31:
                together_word(public_info)
                continue
            # mode == 41 "content":"The  price  of  {}  furniture  is  very  high,  especially  those  pieces  that  were  made  in  Ming  and  Qing  dynasties.","remark":"古董家具的价格很高，尤其是明清时期的家具。"
            # mode == 43  "content":"Reading  is  of  {}  importance  in  language  learning.","remark":"阅读在语言学习中至关重要。" 选时态
            elif mode == 51 or mode == 52 or mode == 53 or mode == 54:
                option = complete_sentence(public_info)
            else:
                print('退出')
                exit(-1)
            submit_exam(public_info, option)
            # sleep 1~5s
            time.sleep(random.randint(1, 5))


def complete_practice(unit: str, progress: int, task_id=None):
    """
    班级任务和自学共用
    :param task_id: 任务id
    :param unit:  单元名称
    :param progress: 单元进度
    :return: None
    """
    main.logger.info(f"获取该{unit}单元的task_id")
    public_info.now_unit = unit
    get_unit_id(public_info)  # return self unit all word
    if task_id:
        public_info.task_id = task_id
    main.logger.info("处理words")
    handle_word_result(public_info)
    main.logger.info("选择该单元所有单词")
    # {"CET4_pre:CET4_pre_10":["survey","apply","defasdfa"]} word
    # not complete unit choice all word
    if progress == 0:
        select_all_word(f"{public_info.course_id}:{unit}", public_info.word_list, public_info.task_id)
    # get first exam
    if task_id:
        get_class_exam(public_info)
    else:
        get_exam(public_info)
    public_info.topic_code = public_info.exam['topic_code']
    main.logger.info("开始答题")
    # topic_mode
    while True:
        main.logger.info("获取题目类型")
        if public_info.exam == 'complete':
            main.logger.info('该单元已完成')
            # unit complete skip next unit
            break
        mode = public_info.exam['topic_mode']
        # handle answer (choice)
        if mode == 0:
            # skip read cord
            jump_read(public_info)
            continue
        elif mode == 32:
            option = select_word(public_info)
        elif mode == 11 or mode == 22:
            option = word_form_mean(public_info)
        elif mode == 31:
            together_word(public_info)
            continue
        elif mode == 51 or mode == 52:
            option = complete_sentence(public_info)

        else:
            option = 0
            main.logger.info(public_info.exam)
            main.logger.info("其他题型,已退出")
            exit(-1)
        # sleep 1~5s
        time.sleep(random.randint(1, 5))
        # submit answer
        if task_id:
            # class task
            submit_exam(public_info, option)
        else:
            submit(public_info, option)


# check token is expire
def init_token():
    # get token
    token = public_info.token
    if token:
        # 验证token 是否过期
        if not verify_token(token):
            get_token(public_info)
    else:
        # use code get token
        get_token(public_info)
    # init requests token
    requests.set_token(public_info.token)


def run():
    init_token()
    main.logger.info('开始答题')
    # class task
    if public_info.is_class_task:
        PublicInfo.task_type = 'ClassTask'
        main.logger.info('开始完成班级任务')
        # get class task
        now_page = 1
        get_class_task(public_info, now_page)
        # get all page
        while public_info.task_total_count > now_page * 10:
            now_page += 1
            get_class_task(public_info, now_page)
        # delete expire task
        filter_expire_task(public_info)
        # start complete class task
        for task_info in public_info.class_task:
            complete_test(task_info)
    # myself task
    if public_info.is_myself_task:
        PublicInfo.task_type = 'StudyTask'
        main.logger.info('开始完成自选任务')
        # get course
        get_select_course(public_info)
        # get all unit
        main.logger.info("获取所有单元的信息")
        get_all_unit(public_info)
        # get not complete
        filler_not_complete_unit(public_info)
        main.logger.info(f"没有完成的单元{public_info.not_complete_unit}")
        for unit, progress in public_info.not_complete_unit.items():
            complete_practice(unit, progress)
    main.logger.info('运行完成')


if __name__ == '__main__':
    # 初始化日志记录
    main = Log("main")
    main.logger.info('开始登录')
    # path
    path = os.path.dirname(__file__)
    # init public info
    main.logger.info("初始化公共组件")
    public_info = PublicInfo(path)
    # run
    run()

import os
import random
import re
import time

import api.request_header as requests
from api.basic_api import get_all_unit, get_unit_id, get_select_course
from api.login import verify_token, get_token
from api.main_api import get_exam, query_word, submit_result, next_exam, select_all_word, get_class_task, \
    get_class_exam, submit_class_exam, next_class_exam
from api.translate import zh_en
from log.log import Log
from publicInfo.publicInfo import PublicInfo
from util.basic_utll import filler_not_complete_unit, filter_expire_task
from util.handle_word_list import handle_word_result
from util.select_mean import select_mean, handle_query_word_mean, filler_option, select_match_word
from util.word_revert import word_revert


# submit
def submit(public_info: PublicInfo, option: int):
    public_info.topic_code = public_info.exam['topic_code']
    # submit result
    submit_result(public_info, option)
    time.sleep(3)
    # get next exam
    next_exam(public_info)


# submit exam
def submit_exam(public_info, option: int or str):
    public_info.topic_code = public_info.exam['topic_code']
    submit_class_exam(public_info, option)
    # get next exam
    next_class_exam(public_info)


# skip read word
def jump_read(public_info):
    time.sleep(random.randint(1, 3))
    main.logger.info("跳过阅读单词卡片")
    next_exam(public_info)
    public_info.topic_code = public_info.exam['topic_code']


# mean form word
def select_word(public_info) -> int or str:
    main.logger.info("汉译英")
    word_mean = public_info.exam['stem']['remark'].replace('……', '')
    main.logger.info(word_mean)
    # option word
    zh_en(public_info, word_mean)
    return ",".join(public_info.zh_en.split())


# word form mean
def word_form_mean(public_info: PublicInfo) -> int:
    main.logger.info("英译汉")
    # is listen
    exam = public_info.exam['stem']['content']
    word = re.findall("{(.*)}", exam)
    # is require regular
    word = word[0] if word else exam
    main.logger.info(f"查询{word}单词意思")
    # word is exist word_list
    if word not in public_info.word_list:
        main.logger.info("将word转原型")
        # word tense trans source
        word = word_revert(word)
    # query word mean
    query_word(public_info, word)
    # filler mean
    handle_query_word_mean(public_info)
    # select option
    main.logger.info('选择意思')
    return select_mean(public_info)


# mean to word
def mean_to_word(public_info):
    # mode 17
    word_mean = public_info.exam['stem']['content']
    # match answer
    return select_match_word(public_info, word_mean)


# select together word
def together_word(public_info):
    main.logger.info("单词搭配")
    # exam options
    options = filler_option(public_info)
    # answer
    result_word = [word['relation'] for word in public_info.exam['stem']['remark']]
    main.logger.info(f"选项{options}")
    main.logger.info(f"答案{result_word}")
    for word in result_word[:2]:
        main.logger.info(f"提交单词:{word}")
        option = options.index(word)
        # submit result
        submit_result(public_info, option)
    next_exam(public_info)
    public_info.topic_code = public_info.exam['topic_code']


# full word
def complete_sentence(public_info):
    main.logger.info("完成单词")
    word_len = public_info.exam['w_lens'][0]
    # submit not  case sensitive
    word_start_with = public_info.exam['w_tip'].lower()
    for word in public_info.word_list:
        if word.startswith(word_start_with):
            main.logger.info(word)
            if len(word) == word_len:
                return word
            elif len(word) + 1 == word_len:
                return word + 's'


def run():
    # init public info
    main.logger.info("初始化公共组件")
    public_info = PublicInfo(path)
    # get token
    token = public_info.token
    if token:
        # 验证token 是否过期
        if not verify_token(token):
            get_token(public_info)
    else:
        # use code get token
        get_token(public_info)
    # init requests
    requests.set_token(public_info.token)
    # get class task
    now_page = 1
    get_class_task(public_info, now_page)
    while public_info.task_total_count > now_page * 10:
        now_page += 1
        get_class_task(public_info, now_page)
    # handle expire task
    filter_expire_task(public_info)
    # start complete class task
    for task_info in public_info.class_task:
        now_unit = task_info['task_name']
        main.logger.info(f'完成{now_unit}')
        # get unit id
        public_info.now_unit = now_unit
        public_info.course_id = task_info['course_id']
        # get all the units of the book
        main.logger.info('获取该书的所有单元')
        get_all_unit(public_info)
        for unit in public_info.all_unit['task_list']:
            if unit['task_name'] == now_unit:
                public_info.now_unit = unit['list_id']
        get_unit_id(public_info)  # return now unit all word 92586275
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
            if mode == 17:
                option = mean_to_word(public_info)
            elif mode == 51:
                option = complete_sentence(public_info)
            else:
                print('退出')
                exit(-1)
            submit_exam(public_info, option)

    # get course
    get_select_course(public_info)
    # get all unit
    main.logger.info("获取所有单元的信息")
    get_all_unit(public_info)
    # get not complete
    filler_not_complete_unit(public_info)
    main.logger.info(f"没有完成的单元{public_info.not_complete_unit}")
    for unit, value in public_info.not_complete_unit.items():
        main.logger.info(f"获取该{unit}单元的task_id")
        public_info.now_unit = unit
        get_unit_id(public_info)  # return self unit all word
        main.logger.info("处理words")
        handle_word_result(public_info)
        main.logger.info("选择该单元所有单词")
        # {"CET4_pre:CET4_pre_10":["survey","apply","defasdfa"]} word
        # not complete unit choice all word
        if value == 0:
            select_all_word(f"{public_info.course_id}:{unit}", public_info.word_list, public_info.task_id)
        # get first exam
        get_exam(public_info)
        public_info.topic_code = public_info.exam['topic_code']
        main.logger.info("开始答题")
        i = 0
        # topic_mode
        while True:
            main.logger.info("获取题目类型")
            if public_info.exam == 'complete':
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
            elif mode == 51:
                option = complete_sentence(public_info)
            else:
                option = 0
                main.logger.info(public_info.exam)
                main.logger.info("其他模式,已退出")
                exit(-1)
            time.sleep(1)
            # submit answer
            submit(public_info, option)
            i += 1


if __name__ == '__main__':
    # 初始化日志记录
    main = Log("main")
    main.logger.info('开始登录')
    # path
    path = os.path.dirname(__file__)
    run()

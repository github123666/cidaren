import os

import api.request_header as requests
from answer_questions.answer_questions import *
from api.basic_api import get_all_unit, get_unit_words, get_select_course, get_book_all_words
from api.login import verify_token, get_token
from api.main_api import get_exam, select_all_word, get_class_task, is_close, skip_exam
from log.log import Log
from publicInfo.publicInfo import PublicInfo
from util.basic_utll import filler_not_complete_unit, filter_expire_task, extract_book_word, query_word_unit
from util.handle_word_list import handle_word_result


def class_task_answer():
    """
    班级任务答题
    :return:
    """
    # get first exam
    get_exam(public_info)
    public_info.topic_code = public_info.exam['topic_code']
    main.logger.info("开始答题")
    while True:
        main.logger.info("获取题目类型")
        if public_info.exam == 'complete':
            # unit complete skip next unit
            break
        mode = public_info.exam['topic_mode']
        main.logger.info(f'题目类型{mode}')
        if mode == 0:
            # skip read cord
            jump_read(public_info)
            continue
        option = answer(public_info, mode)
        if option is None:
            public_info.topic_code = public_info.exam['topic_code']
            skip_exam(public_info)
        else:
            submit(public_info, option)
        # sleep 1~5s
        time.sleep(random.randint(1, 5))


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
    public_info.release_id = task_info['release_id']
    all_test_name = []
    for unit in public_info.all_unit['task_list']:
        unit_name = unit['task_name']
        all_test_name.append(unit_name)
        public_info.all_unit_name.append(unit['list_id'])
        if unit_name == task_name:
            public_info.now_unit = unit['list_id']
            public_info.task_id = unit['task_id']
            break
    unit_progress = task_info['progress']
    # self built test
    if task_name not in all_test_name:
        public_info.is_self_built = True
        main.logger.info(f"{task_name}为自建任务")
        if task_info['task_type'] == 1:
            main.logger.info("完成自学任务的自建任务")
            main.logger.info('获取该自建任务的单词')
            public_info.task_id = task_info['task_id']
            get_unit_words(public_info)
            main.logger.info("获取提交单词")
            query_word_unit(public_info)
            if (unit_progress < 2 and public_info.get_word_list_result['data']['exist_little_task'] != 1) or \
                    public_info.get_word_list_result['data']['exist_little_task'] == 2:
                select_all_word(public_info.word_list, public_info.task_id)
        else:
            main.logger.info("完成班级测试自建任务")
            # get all the words for the book
        get_book_all_words(public_info)
        # extract word
        extract_book_word(public_info)
        # answer
        class_task_answer()
    else:
        if task_info['task_type'] == 1:
            main.logger.info('完成班级任务的自学任务')
            complete_practice(public_info.now_unit, unit_progress, task_info['task_id'])
        else:
            # normal test
            get_unit_words(public_info)  # return now unit all word
            # extract return word
            handle_word_result(public_info)
            public_info.task_id = task_info['task_id']
            class_task_answer()


def complete_practice(unit: str, progress: int, task_id=None):
    """
    班级任务和自学共用
    :param task_id: 任务id
    :param unit:  单元名称
    :param progress: 单元进度
    :return: None
    """
    main.logger.info(f"获取该{unit}单元的单词")
    public_info.now_unit = unit
    public_info.task_id = task_id
    # get all the words in the unit
    get_unit_words(public_info)
    main.logger.info("处理words")
    handle_word_result(public_info)
    main.logger.info("选择该单元所有单词")
    # {"CET4_pre:CET4_pre_10":["survey","apply","defasdfa"]} word
    # not complete unit choice all word
    if (progress < 2 and public_info.get_word_list_result['data']['exist_little_task'] != 1) or \
            public_info.get_word_list_result['data']['exist_little_task'] == 2:
        select_all_word({f"{public_info.course_id}:{unit}": public_info.word_list}, public_info.task_id)
    # get first exam
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
        option = answer(public_info, mode)
        # sleep 1~5s
        if option is None:
            public_info.topic_code = public_info.exam['topic_code']
            skip_exam(public_info)
        else:
            submit(public_info, option)
        # sleep 1~5s
        time.sleep(random.randint(1, 5))


# check token is expire
def init_token():
    # get token
    token = public_info.token
    if token:
        # 验证token 是否过期
        if not verify_token(token):
            get_token(public_info)
        else:
            # init requests token
            requests.set_token(public_info.token)
    else:
        # use code get token
        get_token(public_info)


def run():
    init_token()
    # test(public_info)
    public_info.course_id = 'SZCH'
    get_book_all_words(public_info)
    raise 'test'
    main.logger.info('开始答题')
    # class task
    if public_info.is_class_task:
        PublicInfo.task_type = 'ClassTask'
        PublicInfo.task_type_int = 2
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
            # close self_built test
            public_info.is_self_built = False
            complete_test(task_info)
    # myself task
    if public_info.is_myself_task:
        PublicInfo.task_type = 'StudyTask'
        PublicInfo.task_type_int = 3
        main.logger.info('开始完成自选任务')
        # get course
        get_select_course(public_info)
        # get all unit
        main.logger.info("获取所有单元的信息")
        get_all_unit(public_info)
        # get not complete
        filler_not_complete_unit(public_info)
        main.logger.info(f"没有完成的单元{public_info.not_complete_unit}")
        for unit, progress, task_id in public_info.not_complete_unit:
            # close self_built test
            public_info.is_self_built = False
            complete_practice(unit, progress, task_id)
    main.logger.info('运行完成')
    os.system("pause")


if __name__ == '__main__':
    # 初始化日志记录
    # is delete item
    # if not is_close():
    #     print('项目关闭')
    main = Log("main")
    main.logger.info('开始登录')
    main.logger.info('侵权请联系删除')
    main.logger.info("github123666 <- github.com")
    # path
    path = os.path.dirname(__file__)
    # init public info
    main.logger.info("初始化公共组件")
    public_info = PublicInfo(path)
    # run
    run()

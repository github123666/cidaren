import re
import time

from api.api_all import get_exam, query_word, submit_result, next_exam, get_word_list
from api.translate import zh_en
from log.log import Log
from publicInfo.publicInfo import PublicInfo
from util.handle_word_list import handle_word_result
from util.select_mean import select_mean, handle_query_word_mean, filler_option
from util.word_revert import word_revert


# submit
def submit(public_info: PublicInfo, option: int):
    public_info.topic_code = public_info.exam['topic_code']
    # submit result
    submit_result(public_info, option)
    time.sleep(3)
    # get next exam
    next_exam(public_info)


# mean form word
def select_word(public_info) -> int or str:
    main.logger.info("汉译英")
    word_mean = public_info.exam['stem']['remark']
    print(word_mean)
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


def complete_sentence(public_info):
    main.logger.info("完成单词")
    word_len = public_info.exam['w_lens'][0]
    word_start_with = public_info.exam['w_tip'].lower()
    for word in public_info.word_list:
        if word.startswith(word_start_with) and len(word) == word_len:
            main.logger.info(word)
            return word


def run():
    # init public info
    main.logger.info("初始化公共组件")
    public_info = PublicInfo()
    # get first topic_code
    get_exam(public_info)
    public_info.topic_code = public_info.exam['topic_code']
    main.logger.info("开始答题")
    main.logger.info("获取该单元所有单词")
    get_word_list(public_info)
    main.logger.info("处理words")
    handle_word_result(public_info)
    # main.logger.info("选择该单元所有单词")
    # select_all_word(public_info.word_list)
    i = 0
    # topic_mode
    while 100 > i:
        main.logger.info("获取题目类型")
        mode = public_info.exam['topic_mode']
        if mode == 32:
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
            print(public_info.exam)
            main.logger.info("其他模式,已退出")
            exit(-1)
        time.sleep(1)
        submit(public_info, option)
        i += 1


if __name__ == '__main__':
    # 初始化日志记录
    main = Log("main")
    main.logger.info('开始执行')
    run()

import random
import re
import time

from api.main_api import query_word, submit_result, next_exam
from api.translate import zh_en
from log.log import Log
from publicInfo.publicInfo import PublicInfo
from util.select_mean import select_mean, handle_query_word_mean, filler_option, select_match_word
from util.word_revert import word_revert

query_answer = Log('query_answer')


# submit
def submit(public_info: PublicInfo, option: int or str or dict):
    """
    submit answer
    :param public_info:
    :param option: 选项索引或单词
    :return: None
    """
    public_info.topic_code = public_info.exam['topic_code']
    # submit result
    if type(option) == dict:
        # resolve mode == 31
        for answer_index in option.values():
            submit_result(public_info, answer_index)
    else:
        submit_result(public_info, option)
    #
    time.sleep(random.randint(1, 2))
    # get next exam
    next_exam(public_info)


# skip read word
def jump_read(public_info):
    time.sleep(random.randint(1, 3))
    query_answer.logger.info("跳过阅读单词卡片")
    next_exam(public_info)
    public_info.topic_code = public_info.exam['topic_code']


# mean form word
def select_word(public_info) -> int or str:
    word_mean = public_info.exam['stem']['remark'].replace('……', '')
    query_answer.logger.info("汉译英:" + word_mean)
    # option word
    zh_en(public_info, word_mean)
    query_answer.logger.info(f'汉译英结果: {public_info.zh_en}')
    return ",".join(public_info.zh_en.split())


# word form mean
def word_form_mean(public_info: PublicInfo) -> int:
    query_answer.logger.info("英译汉")
    # is listen
    exam = public_info.exam['stem']['content'].replace(' ', "")
    word = re.findall("{(.*)}", exam)
    # is require regular type 1 is ... xxx {} type2 test
    word = word[0] if word else exam
    query_answer.logger.info(f"查询{word}单词意思")
    # word is exist word_list
    if word not in public_info.word_list:
        query_answer.logger.info("将word转原型")
        # word tense trans source
        word = word_revert(word)
    # query word mean
    query_word(public_info, word)
    # filler mean
    handle_query_word_mean(public_info)
    # select option
    query_answer.logger.info('选择意思')
    return select_mean(public_info)


# mean to word
def mean_to_word(public_info):
    # mode 17
    word_mean = public_info.exam['stem']['content']
    query_answer.logger.info(f'查询{word_mean}意思')
    # match answer
    return select_match_word(public_info, word_mean)


# select together word
def together_word(public_info) -> dict:
    query_answer.logger.info("单词搭配")
    # exam options
    options = filler_option(public_info)
    # answer
    result_word = {word['relation']: options.index(word['relation']) for word in public_info.exam['stem']['remark']}
    query_answer.logger.info(f"选项{options}")
    query_answer.logger.info(f"答案{result_word}")
    return result_word


# full word
def complete_sentence(public_info):
    query_answer.logger.info("补全单词")
    word_len = public_info.exam['w_lens'][0]
    # submit not  case sensitive
    word_start_with = public_info.exam['w_tip'].lower()
    for word in public_info.word_list:
        if word.startswith(word_start_with):
            query_answer.logger.info(word)
            if len(word) == word_len:
                return word
            elif len(word) + 1 == word_len:
                return word + 's'


def answer(public_info, mode):
    if mode == 11:
        option = word_form_mean(public_info)
    elif mode == 15 or mode == 16 or mode == 21 or mode == 22:
        option = word_form_mean(public_info)
    elif mode == 17 or mode == 18:
        option = mean_to_word(public_info)
    elif mode == 31:
        option = together_word(public_info)
    elif mode == 32:
        option = select_word(public_info)
    # mode == 41 "content":"The  price  of  {}  furniture  is  very  high,  especially  those  pieces  that  were  made  in  Ming  and  Qing  dynasties.","remark":"古董家具的价格很高，尤其是明清时期的家具。"
    # mode == 43  "content":"Reading  is  of  {}  importance  in  language  learning.","remark":"阅读在语言学习中至关重要。" 选时态
    elif mode == 51 or mode == 52 or mode == 53 or mode == 54:
        option = complete_sentence(public_info)
    else:
        option = 0
        query_answer.logger.info(public_info.exam)
        query_answer.logger.info("其他题型,程序退出")
        exit(-1)
    return option

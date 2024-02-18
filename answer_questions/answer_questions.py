import random
import re
import time

from api.main_api import query_word, submit_result, next_exam, submit_class_exam, next_class_exam
from api.translate import zh_en
from log.log import Log
from publicInfo.publicInfo import PublicInfo
from util.select_mean import select_mean, handle_query_word_mean, filler_option, select_match_word
from util.word_revert import word_revert

query_answer = Log('query_answer')


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
    query_answer.logger.info("跳过阅读单词卡片")
    next_exam(public_info)
    public_info.topic_code = public_info.exam['topic_code']


# mean form word
def select_word(public_info) -> int or str:
    query_answer.logger.info("汉译英")
    word_mean = public_info.exam['stem']['remark'].replace('……', '')
    query_answer.logger.info(word_mean)
    # option word
    zh_en(public_info, word_mean)
    return ",".join(public_info.zh_en.split())


# word form mean
def word_form_mean(public_info: PublicInfo) -> int:
    query_answer.logger.info("英译汉")
    # is listen
    exam = public_info.exam['stem']['content']
    word = re.findall("{(.*)}", exam)
    # is require regular
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
    # match answer
    return select_match_word(public_info, word_mean)


# select together word
def together_word(public_info):
    query_answer.logger.info("单词搭配")
    # exam options
    options = filler_option(public_info)
    # answer
    result_word = [word['relation'] for word in public_info.exam['stem']['remark']]
    query_answer.logger.info(f"选项{options}")
    query_answer.logger.info(f"答案{result_word}")
    for word in result_word[:2]:
        query_answer.logger.info(f"提交单词:{word}")
        option = options.index(word)
        # submit result
        submit_result(public_info, option)
    next_exam(public_info)
    public_info.topic_code = public_info.exam['topic_code']


# full word
def complete_sentence(public_info):
    query_answer.logger.info("完成单词")
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

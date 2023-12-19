import re
import time

from api.api_all import get_exam, query_word, submit_result,next_exam
from log.log import Log
from publicInfo.publicInfo import PublicInfo
from util.select_mean import select_mean
from util.word_revert import word_revert


def filler_mean(public_info: PublicInfo) -> None:
    means = []
    for mean in public_info.word_query_result['means']:
        means.append(' '.join(mean['mean']))
    public_info.word_means = means


def run():
    # init public info
    main.logger.info("初始化公共组件")
    public_info = PublicInfo()
    # get first topic_code
    get_exam(public_info)
    # 判断 exam是否存在
    # exam =
    i = 0
    while 10 > i:
        public_info.topic_code = public_info.exam['topic_code']
        word = public_info.exam['stem']['content']
        main.logger.info(f"查询{word}单词意思")
        # get word source
        word = word_revert(word)
        # query word
        query_word(public_info, word)
        main.logger.info("开始匹配结果")
        # filler mean
        main.logger.info('过滤出单词意思')
        filler_mean(public_info)
        # submit
        submit_result(public_info, select_mean(public_info))
        time.sleep(3)
        i += 1
        next_exam(public_info)



if __name__ == '__main__':
    # 初始化日志记录
    main = Log("main")
    main.logger.info('开始执行')
    run()

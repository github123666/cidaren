import re

from api.main_api import query_word
from log.log import Log

# log module
select_module = Log("select_module")


#
def handle_query_word_mean(public_info) -> None:
    means = []
    # for mean in public_info.word_query_result['means']:
    for mean in public_info.word_query_result['options']:
        # means.append(' '.join(mean['mean']))
        means.append(mean['content']['mean'])
        means.append(re.sub("（.*）", "", mean['content']['mean']))
    public_info.word_means = means


def filler_option(public_info) -> list:
    # exam options
    options = []
    # filler option
    for option in public_info.exam["options"]:
        options.append(option["content"])
    return options


# match options
def select_mean(public_info) -> int:
    options = filler_option(public_info)
    # match option
    for index, option in enumerate(options, 0):
        for mean in public_info.word_means:
            # exam option content is disorder,re-order
            if sorted(option.replace(" ", '')) == sorted(mean.replace(" ", '')) or mean in option:
                select_module.logger.info(f"匹配选项{option}")
                return index


# extract query word means
def extract_query_means(query_result: dict) -> list:
    means = []
    for mean in query_result['means']:
        means.append(' '.join(mean['mean']))
    return means


# select match word
def select_match_word(public_info, word_mean) -> int:
    options = filler_option(public_info)
    for index, word in enumerate(options, 0):
        # query word mean
        query_word(public_info, word)
        means = extract_query_means(public_info.word_query_result)
        # is match word mean
        for mean in means:
            if sorted(word_mean.replace(" ", '')) == sorted(mean.replace(" ", '')):
                return index
    exit('匹配失败')

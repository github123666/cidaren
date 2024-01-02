import re

from log.log import Log

# log module
select_module = Log("select_module")


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


def select_mean(public_info) -> int:
    options = filler_option(public_info)
    # match option
    for index, option in enumerate(options, 0):
        for mean in public_info.word_means:
            # exam option content is disorder,re-order
            if sorted(option.replace(" ", '')) == sorted(mean.replace(" ", '')) or mean in option:
                select_module.logger.info(f"匹配选项{option}")
                return index

import re

from api.main_api import query_word
from log.log import Log

# log module
select_module = Log("select_module")


#
def handle_query_word_mean(public_info) -> None:
    # {'course_id': 'CET4_pre', 'list_id': 'CET4_pre_03', 'word': 'pack', 'update_version': '2402041319', 'means': [{'mean': ['verb', '收拾（行李）；装（箱）'], 'ph_info': {'ph_en': 'pæk', 'ph_en_url': '/Resource/unitAudio_EN/CET4_pre_03/pack.mp3', 'ph_us': 'pæk', 'ph_us_url': '/Resource/unitAudio_US/CET4_pre_03/pack.mp3'}, 'usages': [{'usage': None, 'phrases': [], 'phrases_infos': [], 'examples': [{'sen_id': '688', 'sen_content': "Mary, I hope you're {packed} and ready to leave.", 'sen_mean_cn': '玛丽，我希望你收拾好行李准备离开。', 'sen_source': '[CET4 07年12月]', 'sen_source_code': 'CET4_0712_LL1_1M_1', 'audio_file': '/CET4_pre_03/pack/688.mp3'}, {'sen_id': '695', 'sen_content': "I've {packed} it, but I can't remember which bag it's in.", 'sen_mean_cn': '我把它装好了，但我记不起它在哪个包里了。', 'sen_source': '[CET4 07年12月]', 'sen_source_code': 'CET4_0712_LL1_4W_3', 'audio_file': '/CET4_pre_03/pack/695.mp3'}, {'sen_id': '562846', 'sen_content': 'We can {pack} a suitcase with flashlights, a radio, food, drinking water and some tools.', 'sen_mean_cn': '我们可以把手电筒、收音机、食物、饮用水和一些工具打包装入手提箱。', 'sen_source': '[CET6 13年06月]', 'sen_source_code': 'CET6_13063_LP2_1_5_01', 'audio_file': '/CET4_pre_03/pack/562846.mp3'}, {'sen_id': '521628', 'sen_content': 'She hurriedly {packed} a bag and bought a train ticket for home.', 'sen_mean_cn': '她赶快收拾了一下手提包，买了车票回家。', 'sen_source': '', 'sen_source_code': '', 'audio_file': '/CET4_pre_03/pack/521628.mp3'}, {'sen_id': '521637', 'sen_content': 'She {packed} her few belongings in a bag and left.', 'sen_mean_cn': '她把她的几件东西装进包里便离开了。', 'sen_source': '', 'sen_source_code': '', 'audio_file': '/CET4_pre_03/pack/521637.mp3'}]}]}, {'mean': ['noun', '包；盒'], 'ph_info': {'ph_en': 'pæk', 'ph_en_url': '/Resource/unitAudio_EN/CET4_pre_03/pack.mp3', 'ph_us': 'pæk', 'ph_us_url': '/Resource/unitAudio_US/CET4_pre_03/pack.mp3'}, 'usages': [{'usage': None, 'phrases': [], 'phrases_infos': [], 'examples': [{'sen_id': '2185', 'sen_content': "Likewise, a married man who smokes more than a {pack} a day is likely to live as long as a divorced man who doesn't smoke.", 'sen_mean_cn': '同样地，一个每天吸烟超过一包的已婚男人很可能和一个不吸烟的离婚男人一样长寿。', 'sen_source': '[CET4 10年12月]', 'sen_source_code': 'CET4_1012_RP2_02_03', 'audio_file': '/CET4_pre_03/pack/2185.mp3'}, {'sen_id': '521639', 'sen_content': 'Each {pack} contains a book and accompanying CD.', 'sen_mean_cn': '每包内装书一本，并附光盘一张。', 'sen_source': '', 'sen_source_code': '', 'audio_file': '/CET4_pre_03/pack/521639.mp3'}, {'sen_id': '562705', 'sen_content': 'Envelopes are cheaper if you buy them in {packs} of 100.', 'sen_mean_cn': '信封如果按每包100个地成包购买会便宜一些。', 'sen_source': '', 'sen_source_code': '', 'audio_file': '/CET4_pre_03/pack/562705.mp3'}]}, {'usage': {'marked': 'a {pack} of <i>sth</i> ', 'text': 'a pack of sth ', 'cn': '一包/盒…', 'eg': 'a {pack} of cigarettes', 'eg_cn': ''}, 'phrases': ['a {pack} of … 一包……'], 'phrases_infos': [{'sen_id': '156901', 'sen_content': 'a {pack} of …', 'sen_mean_cn': '一包……', 'audio_file': '/CET4_pre_03/pack/156901.mp3'}], 'examples': [{'sen_id': '477487', 'sen_content': 'He reached into a drawer for a {pack} of cigarettes.', 'sen_mean_cn': '他把手伸进抽屉里，掏出一包香烟。', 'sen_source': '', 'sen_source_code': '', 'audio_file': '/CET4_pre_03/pack/477487.mp3'}]}]}], 'version': '2', 'has_au': 1, 'au_addr': 'https://resource-cdn.vocabgo.com', 'au_word': 'pack', 'word_info': {'store_status': 0}}
    means = []
    for mean in public_info.word_query_result['means']:
    # for mean in public_info.word_query_result['options']:
        means.append(' '.join(mean['mean']))
        # means.append(mean['content']['mean'])
        # means.append(re.sub("（.*）", "", mean['content']['mean']))
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

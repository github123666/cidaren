import time


def filler_not_complete_unit(public_info) -> None:
    not_complete_unit = []
    for task in public_info.all_unit['task_list']:
        progress = task['progress']
        if progress <= 97:
            not_complete_unit.append([task['list_id'], progress, task['task_id']])
    public_info.not_complete_unit = not_complete_unit


# delete expire task
def filter_expire_task(public_info):
    unexpired_tasks = []
    for tasks in public_info.class_task:
        for task in tasks['records']:
            # over_status 2 no expire over_status expire
            if task['over_status'] == 2:
                # get progress less 100%
                if task['progress'] < 100:
                    unexpired_tasks.append(task)
    public_info.class_task = unexpired_tasks


# create timestamp
def create_timestamp() -> int:
    return int(time.time() * 1000)


def delete_other_char(result: str) -> str:
    delete_list = ['}', '{', ' ...', ' …']
    for delete_str in delete_list:
        result = result.replace(delete_str, '')
    return result.replace(' ', ',')


# extract word
def extract_book_word(public_info):
    public_info.word_list = [d['word'] for d in public_info.get_book_words_data]


# look up the word in the unit
def query_word_unit(public_info):
    all_unit = {}
    # create all unit dict
    for unit in public_info.all_unit_name:
        all_unit.update({public_info.course_id + ':' + unit: []})
    # word classify
    for word_info in public_info.get_word_list_result["data"]['word_list']:
        all_unit[public_info.course_id + ":" + word_info['list_id']].append(word_info['word'])
    # clear unit is null
    all_unit = {key: value for key, value in all_unit.items() if value}
    public_info.word_list = all_unit

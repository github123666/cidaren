def filler_not_complete_unit(public_info) -> None:
    not_complete_unit = {}
    for task in public_info.all_unit['task_list']:
        progress = task['progress']
        if progress <= 97:
            not_complete_unit.update({task['list_id']: progress})
    public_info.not_complete_unit = not_complete_unit


# delete expire task
def filter_expire_task(public_info):
    unexpired_tasks = []
    for tasks in public_info.class_task:
        for task in tasks['records']:
            if task['over_status'] == 2:
                unexpired_tasks.append(task)
    public_info.class_task = unexpired_tasks

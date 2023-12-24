def filler_not_complete_unit(public_info) -> None:
    not_complete_unit = {}
    for task in public_info.all_unit['task_list']:
        progress = task['progress']
        if progress <= 32:
            not_complete_unit.update({task['list_id']: progress})
    public_info.not_complete_unit = not_complete_unit

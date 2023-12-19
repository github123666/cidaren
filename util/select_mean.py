def select_mean(public_info) -> int:
    options = []
    for option in public_info.exam["options"]:
        options.append(option["content"])
    for index, option in enumerate(options, 0):
        for mean in public_info.word_means:
            if sorted(option) == sorted(mean):
                print(option)
                return index

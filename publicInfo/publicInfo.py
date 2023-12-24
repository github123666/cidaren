class PublicInfo:
    def __init__(self):
        self._topic_code = ''
        self.word_query_result = ''
        self.word_means = ''
        self.exam = ''
        # all word
        self.word_list = ''
        self.get_word_list_result: ''
        # translate
        self.zh_en = ''
        # all unit info
        self.all_unit = ''
        self.not_complete_unit = {}
        self.task_id = ''
        self.now_unit = ''

    @property
    # only read
    def topic_code(self):
        return self._topic_code

    @topic_code.setter
    # only write
    def topic_code(self, value):
        self._topic_code = value

    @topic_code.deleter
    # only del
    def topic_code(self):
        del self._topic_code

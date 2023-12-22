class PublicInfo:
    def __init__(self):
        self._topic_code = ''
        self.word_query_result = ''
        self.word_means = ''
        self.exam = ''
        self.word_list = ''
        self.get_word_list_result: ''
        self.zh_en = ''

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

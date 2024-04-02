import json
import os


class PublicInfo:
    task_type: str
    task_type_int: int

    def __init__(self, path):
        self.get_word_list_result = {}
        self.path = path
        with open(os.path.join(self.path, "config", "config.json"), 'r', encoding='utf-8') as f:
            # user config
            user_config = json.load(f)
            self._token = user_config['token']
            self.code = user_config['code']
            self.is_class_task = user_config['class_task']
            self.is_myself_task = user_config['myself_task']
        # query_answer
        self._topic_code = ''
        self.word_query_result = ''
        self.word_means = ''
        self.exam = ''
        # all word
        self.word_list = []
        # translate
        self.zh_en = ''
        # all unit info
        self.all_unit = []
        self.not_complete_unit = {}
        self.task_id = ''
        self.now_unit = ''
        self.course_id = ''
        # class task
        self.class_task = []
        # unit task amount
        self.task_total_count = ''
        self.now_page = ''
        self.release_id = ''
        # self_built
        self.get_book_words_data = []
        self.is_self_built = False  # bool
        self.all_unit_name = []
        self.source_option = []

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

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token):
        self._token = token
        with open(os.path.join(self.path,"config", "config.json"), 'r+', encoding="utf-8") as f:
            data = json.load(f)
            # index move begin cover source file
            f.seek(0)
            data['token'] = token
            f.write(json.dumps(data))

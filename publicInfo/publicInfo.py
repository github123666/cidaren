import json
import os


class PublicInfo:
    def __init__(self, path):
        self.path = path
        with open(os.path.join(self.path, "config.json"), 'r', encoding='utf-8') as f:
            self._token, self.code = json.load(f).values()
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
        # token

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
        with open(os.path.join(self.path, "config.json"), 'r+', encoding="utf-8") as f:
            data = json.load(f)
            # index move begin cover source file
            f.seek(0)
            data['token'] = token
            f.write(json.dumps(data))

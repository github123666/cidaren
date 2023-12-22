import hashlib


def create_sign(data: str) -> str:
    md5 = hashlib.md5()
    md5.update(data.encode("utf-8"))
    return md5.hexdigest()


if __name__ == '__main__':
    print(create_sign('task_id=91158510&word_map={"CET4_pre:CET4_pre_01":["offer","pressure","particular","surface","screen","household","character","variety","regulation","desire","normally","cure","basis","tough","tension","intelligent","identical","wave","conservation","elaborate","variation","historical","prosperity","wise","portrait"]}&chose_err_item=2&timestamp=1703074370806&version=2.6.1.231204ajfajfamsnfaflfasakljdlalkflak'))

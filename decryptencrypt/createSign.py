import hashlib


def create_sign(data: str) -> str:
    md5 = hashlib.md5()
    md5.update(data.encode("utf-8"))
    return md5.hexdigest()


if __name__ == '__main__':
    print(create_sign(
        'time_spent=3417&opt_img_w=1704&opt_font_size=94&opt_font_c=#000000&it_img_w=2002&it_font_size=106&timestamp=1702914853747&topic_code=kld4e4psl9LTmVKRV3l8jGyYoqrHl2dnWmJbqJrM2aKV1cyoolmOaGZhaGdqZL2TkVzAkmJoZGllY2+SanBnbG5uZmmVnGKPvJWWkWOTaGFpb2JvbZeXamidYWljcWlqZ3CXaWdiaWlyam6XnGxrjZNlZJQ=&versions=2.6.1.231204ajfajfamsnfaflfasakljdlalkflak'))

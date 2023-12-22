import base64
import json
import re


def debase64(data: dict):
    # bs64 解码后还是有许多乱码情况,这里用正则去掉
    bs64_str = base64.b64decode(data["data"].encode("utf-8")).decode("utf-8", errors='ignore')
    # 正则小概率还是会报错,bs64解出来前面会乱码
    return json.loads(re.findall("{\".*", bs64_str)[0])

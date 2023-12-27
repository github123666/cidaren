import json

from api.request_header import rqs3_session
from decryptencrypt.encrypt_md5 import encrypt_md5
from log.log import Log
from util.create_timestamp import create_timestamp

# basic url
basic_url = 'https://gateway.vocabgo.com/student/api/'
# log init
login = Log("login")


def get_token(public_info, code: str):
    url = 'Auth/Wechat/LoginByWechatCode'
    timestamp = create_timestamp()
    sign = encrypt_md5(
        f'timestamp={timestamp}&version=2.6.1.231204&wechat_code=041cUPFa1BKYCG0Lz0Ha1br9iG3cUPF8ajfajfamsnfaflfasakljdlalkflak')
    rqs3_session.headers.update({'Usertoken': 'e9a12e34fb67904c2554aa8aebb9d343',
                                 "Referer": f"https://app.vocabgo.com/student/?authorize=2&code={code}&state=STATE"})
    # success code
    # {"code":1,"msg":"success","data":{"auth_type":"UserToken","access":["student_or_teacher"],"token":"c8488f0d370a9097d3ee170260c56","subscribe":"1"},"jv":"0","cv":"0"}
    # fail code
    # {"code":0,"msg":"微信服务异常!","data":null,"jv":"0","cv":"0"}
    data = {"wechat_code": code, "timestamp": timestamp, "version": "2.6.1.231204",
            "sign": sign, "app_type": 1}
    rsp = rqs3_session.post(basic_url + url, data=json.dumps(data)).json()
    rsp_data = rsp['data']
    if rsp_data:
        public_info.token = rsp_data['token']
    else:
        login.logger.info("code 已经被试用请重新抓取")


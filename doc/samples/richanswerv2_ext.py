# -*- coding: UTF-8 -*-
import datetime, hashlib, hmac
import requests # Command to install: `pip install request`
import json, sys, time, base64

# 开放平台提供的appkey/accessToken，请填入自己的appkey
appkey = "XXXX";
accessToken = b"YYYYY";


usage = '''
####
#   usage:
#   python richanswerV2.py Path
#   Path, 文件路径
####
'''

if (2 > len(sys.argv)) :
    print (usage);
    sys.exit(0);

# ***** 第一步: 拼接请求数据和时间戳 *****

## 获取请求数据(也就是HTTP请求的Body)
postData = '''
{
    "header": 
    {
        "device": {
            "serial_num":"myserial"
        },
        "qua": "QV=3&PL=ADR&PR=chvoice&VE=7.6&VN=3350&PP=com.tencent.mtt&DE=TV",
        "lbs":
        {
            "latitude":30.5434, 
            "longitude":104.068
        }
    },
    "payload": {
        "query": "",
        "semantic": {
            "domain":"image_recognition",
            "intent":"image_figures"
        },
        "extra_data": [
            {
                "type":"IMAGE",
                "data_base64":""
            }
        ]
    }
}
'''

jsonReq = json.loads(postData);
if (2 >= len(sys.argv)) :
    file = open(sys.argv[1], "rb");
    data = file.read();
    if (0 < len(data)) :
        jsonReq["payload"]["extra_data"][0]["data_base64"] = base64.b64encode(data).decode();

## 使用requests.session保持长连接
session = requests.session()

## 获得ISO8601时间戳
credentialDate = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')

## 拼接数据
signingContent = json.dumps(jsonReq) + credentialDate

# ***** 第二步: 获取Signature签名 *****
signature = hmac.new(botSecret, signingContent.encode('utf-8'), hashlib.sha256).hexdigest()

# ***** 第三步: 组装Authorization，在HTTP请求头中带上签名信息
authorizationHeader = 'TVS-HMAC-SHA256-BASIC' + ' ' + 'CredentialKey=' + botKey + ', ' + 'Datetime=' + credentialDate + ', ' + 'Signature=' + signature

headers = {'Content-Type': 'application/json; charset=UTF-8', 'Authorization': authorizationHeader}

# **** 发送请求 *****
requestUrl = 'https://aiwx.html5.qq.com/api/v1/richanswerV2'

print ('Begin request...')
print ('Request Url = ' + requestUrl)


session.headers.update(headers)
print ('Request Headers =' + str(session.headers))
print ('Request Body =' + json.dumps(jsonReq))

reqTime = time.time();
r = session.post(requestUrl, data = json.dumps(jsonReq).encode('utf-8'))
respTime = time.time();

print ('Response...')
print ("HTTP Status Code:%d" % r.status_code, "cost:%f(ms)" %((respTime - reqTime) * 1000));
print (r.text)
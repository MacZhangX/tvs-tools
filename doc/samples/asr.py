# -*- coding: UTF-8 -*-
import datetime, hashlib, hmac
import requests # Command to install: `pip install requests`
import json
import base64
import time
import sys

usage = '''
####
#   usage:
#   python asr.py Infile
#   Infile, 输入WAV文件
####
'''

if (2 > len(sys.argv)) :
    print (usage);
    sys.exit(0);

# 开放平台提供的appkey/accessToken，请填入自己的appkey
appkey = "XXXX";
accessToken = b"YYYY";

# ***** Task 1: 拼接请求数据和时间戳 *****

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
    "payload": 
    {
        "voice_meta":
        {
            "compress":"PCM",
            "sample_rate":"16K",
            "channel":1
        },
        "session_id":"",
        "index":0,
        "voice_finished":false,
        "voice_base64":""
    }
}
'''



# **** Send the request *****
requestUrl = 'https://aiwx.html5.qq.com/api/asr'

print ('Begin request...')
print ('Request Url = ' + requestUrl)

## 使用requests.session保持长连接
session = requests.session();

jsonReq = json.loads(postData);
offset = 0;
file = open(sys.argv[1], "rb");
fileData = file.read();
file.close();
file = open(sys.argv[1], "rb");
## WAV文件前44字节是头信息，跳过。
file.read(44);
    
while 1 :
    # ***** 第一步: 拼接请求数据和时间戳 *****
    ## 获得ISO8601时间戳
    credentialDate = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')

    data = file.read(3200);
    base64Data = base64.b64encode(data).decode();
    jsonReq["payload"]["voice_base64"] = base64Data;
    print("read length:" + str(len(data)));
    if (len(data) < 3200) :
        jsonReq["payload"]["voice_finished"] = True;
        
    offset += len(data);
    ## 拼接数据
    signingContent = json.dumps(jsonReq) + credentialDate;

    # ***** 第二步: 获取Signature签名 *****
    signature = hmac.new(accessToken, signingContent.encode('utf-8'), hashlib.sha256).hexdigest()

    # ***** 第三步: 组装Authorization，在HTTP请求头中带上签名信息
    authorizationHeader = 'TVS-HMAC-SHA256-BASIC' + ' ' + 'CredentialKey=' + appkey + ', ' + 'Datetime=' + credentialDate + ', ' + 'Signature=' + signature

    headers = {'Content-Type': 'application/json; charset=UTF-8', 'Authorization': authorizationHeader};
    
    session.headers.update(headers);
    # **** Send the request *****
    
    reqTime = time.time();
    r = session.post(requestUrl, data = json.dumps(jsonReq).encode('utf-8'));
    respTime = time.time();

    print ("reqTime:%f" % reqTime, "respTime:%f" % respTime); 
    print ('Response...')
    print ('HTTP Status Code:%d' % r.status_code, 'cost:%f(ms)' %((respTime - reqTime) * 1000))

    if 200 != r.status_code : 
        file.close();
        print("response body:"+r.text);
        print("出错了！");
        break;

    jsonResp = json.loads(r.text);
    print("result:" + jsonResp["payload"]["result"]);
    
    if True == jsonResp["payload"]["final_result"] or True == jsonReq["payload"]["voice_finished"]:
        file.close();
        print("结束了！");
        break;
    else :
        if 0 == len(jsonResp["header"]["session"]["session_id"]) :
            file.close();
            print("出错了!");
            break;
        else :
            jsonReq["payload"]["session_id"] = jsonResp["header"]["session"]["session_id"];
            jsonReq["payload"]["index"] = offset;
            
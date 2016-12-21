#coding: utf8
import json
import httplib, urllib
import web

def translate_baidu(word):
    count = web.utils.counter()
    params = "from=en&to=zh&query=%s&transtype=realtime&simple_means_flag=3" % urllib.quote(word)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    httpClient = httplib.HTTPConnection("fanyi.baidu.com", 80, timeout=10)
    httpClient.request("POST", "/v2transapi", params, headers)
    response = httpClient.getresponse()
    #print response.status
    #print response.reason
    #print '-----'
    text = response.read()
    httpClient.close()

    obj = json.loads(text)
    json_text_double = obj['liju_result']['double']

    trans_result = obj['trans_result']['data'][0]['dst']
    count.add(trans_result)
    count.add(trans_result)

    tag_result = obj['liju_result']['tag']
    for tag in tag_result:
        count.add(tag)
        count.add(tag)

    if not json_text_double:
        return []
    obj2 = json.loads(json_text_double)

    for case in obj2:
        tmp = ''
        for segs in case[1]:
            if segs[3] == 1:
                tmp += segs[0]
        tmp = tmp.replace(u'。', '').replace(u'，', '').replace(' ',
                '').replace(',', '')
        count.add(tmp)

    res = [x for x in count.items() if x[1] > 1 and x[0].strip()]
    res.sort(key = lambda x:-x[1])
    #for w, n in res:
    #    print w, n, type(w)
    return res

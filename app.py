import json
import math
import time
import web
import leancloud
from leancloud import User
from grabber import translate_baidu

app = web.application()
TryWords = leancloud.Object.extend('TryWords')
GetWords = leancloud.Object.extend('GetWords')

def diac_trim(text):
    ulist = [u for u in text if ord(u) < 128]
    return ''.join(ulist)


class Home:
    def GET(self, text):
        text = diac_trim(text)
        ret = [x[0] for x in translate_baidu(text)]
        return '; '.join(ret)


class Login:
    def POST(self):
        it = web.input()
        username = it.get('username', '')
        password = it.get('password', '')
        user = User()
        try:
            user.login(username, password)
            token = user.get_session_token()
            web.setcookie('token', token)
            return {'code': 0, 'token': token}
        except leancloud.errors.LeanCloudError:
            return {'code': 1}


class AddWord:
    def POST(self):
        it = web.input()
        try:
            word = it.get('word')
            context = it.get('context')
            expl = it.get('expl')
            token = it.get('token')
            now = int(it.get('now', time.time()))
            user = User().become(token)
        except leancloud.errors.LeanCloudError:
            return {'code': 1}
        delay = math.exp(math.log(30) / (user.get('avgGetCount') - 0.1)) * 86400
        recall_day = int((now + 8 * 3600 + delay) / 86400)
        obj = TryWords()
        obj.set('word', word)
        obj.set('context', context)
        obj.set('userId', user.id)
        obj.set('expl', expl)
        obj.set('delay', delay)
        obj.set('tryCount', 0)
        obj.set('recallDay', recall_day)
        obj.set('startTime', now)
        obj.save()
        return {'code': 0}


class TestWord:
    def POST(self):
        it = web.input()
        try:
            grade = it.get('grade')
            token = it.get('token')
            tryId = it.get('tryId')
            now = int(it.get('now', time.time()))
            user = User().become(token)
        except leancloud.errors.LeanCloudError:
            return {'code': 1}
        obj = TryWords.query.get(tryId)
        delay = obj.get('delay')
        tryCount = obj.get('tryCount')
        if grade == 'c':
            delay = delay / 2.0
        elif grade == 'b':
            delay = delay / 1.1
        elif grade == 'a':
            if delay > 30 * 86400 - 1:
                getObj = GetWords()
                getObj.set('userId', user.id)
                getObj.set('wordAndExpl', obj.get('word')+'|'+obj.get('expl'))
                getObj.set('tryCount', obj.get('tryCount') + 1)
                getObj.set('totalTime', now - obj.get('startTime'))
                getObj.save()
                obj.destroy()
                return {'code': 0}
            delay *= math.exp(math.log(30) / (user.get('avgGetCount') - 0.1))
            delay = min(delay, 40 * 86400)
        recall_day = int((now + 8 * 3600 + delay) / 86400)
        obj.set('delay', delay)
        obj.set('tryCount', tryCount + 1)
        obj.set('recallDay', recall_day)
        obj.save()
        return {'code': 0}


def all_wrapper(laber):
    ret = laber()
    web.header('Access-Control-Allow-Origin', '*')
    if isinstance(ret, dict):
        web.header('Content-Type', 'application/json')
        return json.dumps(ret)
    return ret


app.add_mapping("/btrans/(.+)", Home)
app.add_mapping("/login", Login)
app.add_mapping("/word/add", AddWord)
app.add_mapping("/word/test", TestWord)
app.add_processor(all_wrapper)


if __name__ == "__main__":
    print app.request("/btrans/satirised").data
    #app.run()

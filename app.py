import web
from grabber import translate_baidu

app = web.application()


def diac_trim(text):
    ulist = [u for u in text if ord(u) < 128]
    return ''.join(ulist)


class Home:
    def GET(self, text):
        text = diac_trim(text)
        ret = [x[0] for x in translate_baidu(text)]
        web.header('Access-Control-Allow-Origin', '*')
        return '; '.join(ret)


app.add_mapping("/btrans/(.+)", Home)

if __name__ == "__main__":
    print app.request("/btrans/mayor").data
    #app.run()

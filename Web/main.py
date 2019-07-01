from fanic import route, app
from sanic.response import html
from lazy.ef_app import EfApp
from lazy.effect import lazy
from article import Article
from time import sleep
import asyncio
import threading
from crol import get_right_nobel

html_file = open("./main.html", 'r', encoding="utf-8")
lines = html_file.readlines()
main_page = ""
for i in lines:
    main_page += i
main_page += ""


ws_file = open("./ws.html", 'r', encoding="utf-8")
lines = ws_file.readlines()
ws_page = ""
for i in lines:
    ws_page += i
ws_page += ""


progress_table = {}

@lazy
def home(req):
    return html(main_page)


@app.route("/nobel/<blog>/<article>/<no>")
async def nobel(req, blog, article, no):
    article = Article(blog, article, no)
    progress_table[article.name] = article
    
    ws = ws_page.replace("HASHDATA", article.name)
    return html(ws)


@app.websocket('/feed')
async def feed(request, ws):
    article = await ws.recv()
    t = threading.Thread(target=lambda: get_right_nobel(progress_table[article]))
    t.start()
    while True:
        await ws.send(progress_table[article].now_state)
        sleep(3)
        if progress_table[article].now_state == 100:
            break

@EfApp
def main():
    route('/', home)
    app.static('/static', './static', content_type='text/html; charset=utf-8')
    app.run(host="0.0.0.0", port=8000)
    return

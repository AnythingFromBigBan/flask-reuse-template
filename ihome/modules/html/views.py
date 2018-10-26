from ihome import sr
from ihome.modules.html import html_blu


# 2.使用蓝图注册路由
@html_blu.route('/')
def index():
    sr.set("name", "lisi")
    return "index"
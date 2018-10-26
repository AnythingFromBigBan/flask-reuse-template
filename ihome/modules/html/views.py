from ihome.modules.html import html_blu


# 2.使用蓝图注册路由
@html_blu.route('/')
def index():
    return "index"
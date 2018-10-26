from ihome import sr
from ihome.modules.html import html_blu
import logging  # python内置的日志模块  将日志信息在控制台中输出, 并且可以将日志保存到文件中
# flask中的默认日志也是集成的logging模块, 但是没有将日志保存到文件中
from flask import current_app


# 2.使用蓝图注册路由
@html_blu.route('/')
def index():
    # logging.error("出现了一个错误")  # logging默认的输出不包含错误位置, 显示效果不好, 可以使用flask内置的日志输出语法来代替
    current_app.logger.error("出现了一个错误")
    return "index"
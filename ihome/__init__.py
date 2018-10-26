from flask import Flask
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis

from config import config_dict
from ihome.modules.html import html_blu


# 定义函数 封装应用的创建和配置  工厂函数(调用者提供生产物料, 函数内部封装创建过程)
def create_app(config_type):
    app = Flask(__name__)

    # 根据配置类型取出配置类
    config_class = config_dict.get(config_type)

    # 从对象加载配置信息
    app.config.from_object(config_class)

    # 创建数据库连接对象
    db = SQLAlchemy(app)
    # 创建redis连接对象
    sr = StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)

    # 初始化session存储对象
    Session(app)
    # 初始化迁移器
    Migrate(app, db)

    # 3. 注册蓝图
    app.register_blueprint(html_blu)
    return app
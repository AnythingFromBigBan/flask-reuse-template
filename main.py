from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis

app = Flask(__name__)

class Config:
    # 设置配置同名的类属性
    DEBUG = True  # 设置调试模式
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/ihome"  # 设置数据库连接地址
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否追踪数据库变化
    REDIS_HOST = "127.0.0.1"  # redis的ip
    REDIS_PORT = 6379  # redis的端口


app.config.from_object(Config)
# 创建数据库连接
db = SQLAlchemy(app)
# 创建redis连接对象
sr = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)


@app.route('/')
def index():
    sr.set("name", "zs")
    return "index"


if __name__ == '__main__':
    app.run()
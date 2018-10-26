from datetime import timedelta

from flask import Flask, session
from flask_session import Session
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
    SESSION_TYPE = "redis"  # session存储类型  性能好 方便设置过期时间
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # redis连接对象
    SESSION_USE_SIGNER = True  # 设置sessionid加密  如果加密, 必须设置应用秘钥
    SECRET_KEY = "QLDEP2v5YstktI0qP8SEk3MowGCG4KCegZKhYgZq33HB9dUV0Vb7FVzg30QLf16V"  # 设置应用秘钥
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)  # 设置session过期时间  默认支持设置过期时间


app.config.from_object(Config)
# 创建数据库连接
db = SQLAlchemy(app)
# 创建redis连接对象
sr = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

# 初始化session存储对象
Session(app)


@app.route('/')
def index():
    session["age"] = 20
    return "index"


if __name__ == '__main__':
    app.run()
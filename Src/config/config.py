import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(ROOT_DIR, BASE_DIR)


HOST_NAME = "http://127.0.0.1:5001"
UPLOAD_FILE_PATH = "/static/upload/"


class CommonConfig(object):
    SECRET_KEY = os.urandom(24)
    # # session相关配置，并将session中的数据保存到redis
    # SESSION_TYPE = 'redis'


class DevelopConfig(CommonConfig):
    # 配置Debug模式为 True
    DEBUG = True

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
        'mysql', 'pymysql', 'alex', 'yl952001', '120.55.63.27', '3306', 'nia2.0')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductConfig(CommonConfig):
    DEBUG = False


class TestConfig(CommonConfig):
    DEBUG = False

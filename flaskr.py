# -*- coding: utf-8 -*-
# @author:Alex-PC
# @file: flaskr.py
# @time: 2019/03/14

from flask_restful import Api
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from Src.common.models import db
from Src.controllers.auth_controller import AuthController
from Src.controllers.db_controller import DBController
from Src.utils.app import create_app

# 创建程序实例
app = create_app()
# 初始化第三方库
db.init_app(app=app)
api = Api(app=app)
migrate = Migrate(app=app, db=db)
manager = Manager(app=app)
manager.add_command("db", MigrateCommand)

# 注册接口
api.add_resource(DBController, r"/v1/api/db/")
api.add_resource(AuthController, r"/v1/api/auth/")


@app.route("/index/")
def index():
    return "hello"


if __name__ == "__main__":
    print(app.url_map)
    manager.run()

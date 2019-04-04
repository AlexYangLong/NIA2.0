import os
from flask import Flask
from flask_restful import Api

from Src.config.config import ROOT_DIR, DevelopConfig
from Src.controllers.address_controller import AddressController
from Src.controllers.capriccio_controller import CapriccioController
from Src.controllers.comment_controller import CommentController
from Src.controllers.diary_controller import DiaryController
from Src.controllers.essay_controller import EssayController
from Src.controllers.impression_controller import ImpressionController
from Src.controllers.user_controller import RegisterController, LoginController, UserInfoController, UserPwdController, \
    ResetPwdController


def create_app():
    # 获取模板、静态文件路径
    templates_dir = os.path.join(ROOT_DIR, "Web/templates")
    static_dir = os.path.join(ROOT_DIR, "Web/static")
    # 应用程序实例
    app = Flask(__name__, template_folder=templates_dir, static_folder=static_dir)
    # app = Flask(__name__)
    # 加载配置信息
    app.config.from_object(DevelopConfig)

    api = Api(app=app)
    api.add_resource(RegisterController, r"/v1/bms/user/register/")
    api.add_resource(LoginController, r"/v1/bms/user/login/")
    api.add_resource(UserInfoController, r"/v1/bms/user/<int:uid>/", r"/v1/bms/user/")
    api.add_resource(UserPwdController, r"/v1/bms/user/password/")
    api.add_resource(ResetPwdController, r"/v1/bms/user/<int:uid>/password/")
    api.add_resource(EssayController, r"/v1/bms/essay/<int:eid>/", r"/v1/bms/essay/")
    api.add_resource(CommentController, r"/v1/bms/comment/", r"/v1/bms/comment/<int:cid>/")
    api.add_resource(ImpressionController, r"/v1/bms/impression/<int:imid>/", r"/v1/bms/impression/")
    api.add_resource(DiaryController, r"/v1/bms/diary/<int:did>/", r"/v1/bms/diary/")
    api.add_resource(CapriccioController, r"/v1/bms/capriccio/<int:cid>/", r"/v1/bms/capriccio/")
    api.add_resource(AddressController, r"/v1/bms/address/<int:aid>/", r"/v1/bms/address/")

    return app

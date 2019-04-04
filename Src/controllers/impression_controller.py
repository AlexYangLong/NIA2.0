# -*- coding: utf-8 -*-
# @author:Alex-PC
# @file: impression_controller.py
# @time: 2019/03/15
from flask import request
from flask_restful import Resource

from Src.common import status_code
from Src.services.impression_service import ImpressionService
from Src.utils import check_utils
from Src.utils.decorator import write_operate_log
from Src.utils import log as logger


class ImpressionController(Resource):
    @staticmethod
    @write_operate_log(action_cn="获取读后感", action_en="Get impression or list")
    def get(imid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/impression/([1-9][0-9]*)/$", r"^/v1/bms/impression/$"]):
            return status_code.URL_ERROR
        try:
            impression_service = ImpressionService()
            if imid:
                impression = impression_service.get_impression_by_id(impression_id=imid)
                if not impression:
                    return status_code.IMPRESSION_NOT_EXIST
                result = status_code.SUCCESS
                # impression["cover"] = os.path.join(ROOT_DIR, "Web/static/" + impression["cover"])
                impression["cover"] = "".join(["http://", "127.0.0.1:5001", "/static/", impression["cover"]])
                result["data"] = impression
                return result
            else:
                data = request.args
                if not (isinstance(data, dict) and data.get("pn") and data.get("ps")):
                    return status_code.ARGS_PARAMS_ERROR
                if not (data.get("pn").isdigit() and data.get("pn").isdigit()):
                    raise Exception("请求参数pn和ps必须是整数")
                page_size = int(data.get("ps"))
                page_now = int(data.get("pn"))
                user_id = request.form.get('user_id')
                if not data.get("title"):
                    impression_list = impression_service.get_all_impression_by_page(user_id=user_id,
                                                                                    page_now=page_now,
                                                                                    page_size=page_size)
                else:
                    impression_list = impression_service.get_impression_by_title_page(title=data.get("title"),
                                                                                      page_now=page_now,
                                                                                      page_size=page_size)
                result = status_code.SUCCESS
                for impression in impression_list:
                    # impression["cover"] = os.path.join(ROOT_DIR, "Web/static/" + impression["cover"])
                    impression["cover"] = "http://127.0.0.1:5001/static/" + impression["cover"]
                result["data"] = impression_list
                return result
        except Exception as ex:
            print(ex)
            logger.error("获取读后感失败,{}".format(ex))
            return status_code.FAIL

    @staticmethod
    @write_operate_log(action_cn="创建读后感", action_en="Create impression")
    #@login_required
    def post(imid=None):
        pass

    @staticmethod
    @write_operate_log(action_cn="修改读后感", action_en="Update impression")
    #@login_required
    def put(imid=None):
        pass

    @staticmethod
    @write_operate_log(action_cn="删除读后感", action_en="Delete impression")
    #@login_required
    def delete(imid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/impression/$"]):
            return status_code.URL_ERROR
        data = request.json
        if not (data and isinstance(data, dict)) or not isinstance(data.get("ids"), list):
            return status_code.JSON_PARAMS_ERROR
        if not data.get("ids"):
            return {"code": status_code.REQUIRED_PARAM_CODE,
                    "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format("读后感id"),
                    "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format("impression ids")}
        try:
            impression_service = ImpressionService()
            impression_service.delete_impression(impression_id_list=data.get("ids"))
            return status_code.SUCCESS
        except Exception as ex:
            print(ex)
            logger.error("删除读后感失败,{}".format(ex))
            return status_code.FAIL

# -*- coding: utf-8 -*-
# @author:Alex-PC
# @file: capriccio_controller.py
# @time: 2019/03/15
from flask import request
from flask_restful import Resource

from Src.common import status_code
from Src.services.capriccio_service import CapriccioService
from Src.utils import check_utils
from Src.utils.decorator import write_operate_log
from Src.utils import log as logger


class CapriccioController(Resource):
    @staticmethod
    @write_operate_log(action_cn="获取随想", action_en="Get capriccio or list")
    def get(cid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/capriccio/([1-9][0-9]*)/$", r"^/v1/bms/capriccio/$"]):
            return status_code.URL_ERROR
        try:
            capriccio_service = CapriccioService()
            if cid:
                capriccio = capriccio_service.get_capriccio_by_id(capriccio_id=cid)
                if not capriccio:
                    return status_code.CAPRICCIO_NOT_EXIST
                result = status_code.SUCCESS
                # capriccio["cover"] = os.path.join(ROOT_DIR, "Web/static/" + capriccio["cover"])
                capriccio["cover"] = "".join(["http://", "127.0.0.1:5001", "/static/", capriccio["cover"]])
                result["data"] = capriccio
                return result
            else:
                data = request.args
                if not (isinstance(data, dict) and data.get("pn") and data.get("ps")):
                    return status_code.ARGS_PARAMS_ERROR
                if not (data.get("pn").isdigit() and data.get("pn").isdigit()):
                    raise Exception("请求参数pn和ps必须是整数")
                page_size = int(data.get("ps"))
                page_now = int(data.get("pn"))
                if not data.get("title"):
                    capriccio_list = capriccio_service.get_all_capriccio_by_page(page_now=page_now,
                                                                                 page_size=page_size)
                else:
                    capriccio_list = capriccio_service.get_capriccio_by_title_page(title=data.get("title"),
                                                                                   page_now=page_now,
                                                                                   page_size=page_size)
                result = status_code.SUCCESS
                for capriccio in capriccio_list:
                    # capriccio["cover"] = os.path.join(ROOT_DIR, "Web/static/" + capriccio["cover"])
                    capriccio["cover"] = "http://127.0.0.1:5001/static/" + capriccio["cover"]
                result["data"] = capriccio_list
                return result
        except Exception as ex:
            print(ex)
            logger.error("获取随想失败,{}".format(ex))
            return status_code.FAIL

    @staticmethod
    @write_operate_log(action_cn="创建随想", action_en="Create capriccio")
    #@login_required
    def post(cid=None):
        pass

    @staticmethod
    @write_operate_log(action_cn="修改随想", action_en="Update capriccio")
    #@login_required
    def put(cid=None):
        pass

    @staticmethod
    @write_operate_log(action_cn="删除随想", action_en="Delete capriccio")
    #@login_required
    def delete(cid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/capriccio/$"]):
            return status_code.URL_ERROR
        data = request.json
        if not (data and isinstance(data, dict)) or not isinstance(data.get("ids"), list):
            return status_code.JSON_PARAMS_ERROR
        if not data.get("ids"):
            return {"code": status_code.REQUIRED_PARAM_CODE,
                    "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format("随想id"),
                    "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format("capriccio ids")}
        try:
            capriccio_service = CapriccioService()
            capriccio_service.delete_capriccio(capriccio_id_list=data.get("ids"))
            return status_code.SUCCESS
        except Exception as ex:
            print(ex)
            logger.error("删除随想失败,{}".format(ex))
            return status_code.FAIL

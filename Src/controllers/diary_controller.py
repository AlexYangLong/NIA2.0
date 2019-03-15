# -*- coding: utf-8 -*-
# @author:Alex-PC
# @file: impression_controller.py
# @time: 2019/03/15
from flask import request
from flask_restful import Resource

from Src.common import status_code
from Src.services.diary_service import DiaryService
from Src.utils import check_utils
from Src.utils.decorator import write_operate_log
from Src.utils import log as logger


class DiaryController(Resource):
    @staticmethod
    @write_operate_log(action_cn="获取日记", action_en="Get diary or list")
    def get(did=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/diary/([1-9][0-9]*)/$", r"^/v1/bms/diary/$"]):
            return status_code.URL_ERROR
        try:
            diary_service = DiaryService()
            if did:
                diary = diary_service.get_diary_by_id(diary_id=did)
                if not diary:
                    return status_code.DIARY_NOT_EXIST
                result = status_code.SUCCESS
                # essay["cover"] = os.path.join(ROOT_DIR, "Web/static/" + essay["cover"])
                diary["cover"] = "".join(["http://", "127.0.0.1:5001", "/static/", diary["cover"]])
                result["data"] = diary
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
                    diary_list = diary_service.get_all_diary_by_page(page_now=page_now,
                                                                     page_size=page_size)
                else:
                    diary_list = diary_service.get_diary_by_title_page(title=data.get("title"),
                                                                       page_now=page_now,
                                                                       page_size=page_size)
                result = status_code.SUCCESS
                for diary in diary_list:
                    # diary["cover"] = os.path.join(ROOT_DIR, "Web/static/" + essay["cover"])
                    diary["cover"] = "http://127.0.0.1:5001/static/" + diary["cover"]
                result["data"] = diary_list
                return result
        except Exception as ex:
            print(ex)
            logger.error("获取日记失败,{}".format(ex))
            return status_code.FAIL

    @staticmethod
    @write_operate_log(action_cn="创建日记", action_en="Create diary")
    #@login_required
    def post(did=None):
        pass

    @staticmethod
    @write_operate_log(action_cn="修改日记", action_en="Update diary")
    #@login_required
    def put(did=None):
        pass

    @staticmethod
    @write_operate_log(action_cn="删除日记", action_en="Delete diary")
    #@login_required
    def delete(did=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/diary/$"]):
            return status_code.URL_ERROR
        data = request.json
        if not (data and isinstance(data, dict)) or not isinstance(data.get("ids"), list):
            return status_code.JSON_PARAMS_ERROR
        if not data.get("ids"):
            return {"code": status_code.REQUIRED_PARAM_CODE,
                    "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format("日记id"),
                    "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format("diary ids")}
        try:
            diary_service = DiaryService()
            diary_service.delete_diary(diary_id_list=data.get("ids"))
            return status_code.SUCCESS
        except Exception as ex:
            print(ex)
            logger.error("删除日记失败,{}".format(ex))
            return status_code.FAIL

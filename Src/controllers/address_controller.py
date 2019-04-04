# -*- coding: utf-8 -*-
# @author:Alex
# @file: address_controller.py
# @time: 2019/04/04

from flask import request
from flask_restful import Resource

from Src.common import status_code
from Src.services.address_service import AddressService
from Src.utils import check_utils
from Src.utils.decorator import write_operate_log
from Src.utils import log as logger


class AddressController(Resource):
    @staticmethod
    @write_operate_log(action_cn="获取通讯录", action_en="Get address or list")
    def get(aid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/address/([1-9][0-9]*)/$", r"^/v1/bms/address/$"]):
            return status_code.URL_ERROR
        try:
            address_service = AddressService()
            if aid:
                address = address_service.get_address_by_id(address_id=aid)
                if not address:
                    return status_code.ADDRESS_NOT_EXIST
                result = status_code.SUCCESS
                # address["cover"] = os.path.join(ROOT_DIR, "Web/static/" + address["cover"])
                # address["cover"] = "".join(["http://", "127.0.0.1:5001", "/static/", address["cover"]])
                result["data"] = address
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
                if not data.get("link_name"):
                    address_list = address_service.get_all_address_by_page(user_id=user_id,
                                                                           page_now=page_now,
                                                                           page_size=page_size)
                else:
                    address_list = address_service.get_address_by_title_page(link_name=data.get("link_name"),
                                                                             page_now=page_now,
                                                                             page_size=page_size)
                result = status_code.SUCCESS
                # for address in address_list:
                #     # address["cover"] = os.path.join(ROOT_DIR, "Web/static/" + address["cover"])
                #     address["cover"] = "http://127.0.0.1:5001/static/" + address["cover"]
                result["data"] = address_list
                return result
        except Exception as ex:
            print(ex)
            logger.error("获取通讯录失败,{}".format(ex))
            return status_code.FAIL

    @staticmethod
    @write_operate_log(action_cn="创建通讯录", action_en="Create address")
    #@login_required
    def post(aid=None):
        pass

    @staticmethod
    @write_operate_log(action_cn="修改通讯录", action_en="Update address")
    #@login_required
    def put(aid=None):
        pass

    @staticmethod
    @write_operate_log(action_cn="删除通讯录", action_en="Delete address")
    #@login_required
    def delete(aid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/address/$"]):
            return status_code.URL_ERROR
        data = request.json
        if not (data and isinstance(data, dict)) or not isinstance(data.get("ids"), list):
            return status_code.JSON_PARAMS_ERROR
        if not data.get("ids"):
            return {"code": status_code.REQUIRED_PARAM_CODE,
                    "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format("通讯录id"),
                    "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format("address ids")}
        try:
            address_service = AddressService()
            address_service.delete_address(address_id_list=data.get("ids"))
            return status_code.SUCCESS
        except Exception as ex:
            print(ex)
            logger.error("删除通讯录失败,{}".format(ex))
            return status_code.FAIL


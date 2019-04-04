# -*- coding: utf-8 -*-
# @author:Alex-PC
# @file: address_service.py
# @time: 2019/04/04

from Src.common.model import Address
from Src.common.service import session_scope
from Src.utils.check_utils import check_param_format


class AddressService(object):

    def create_address(self, user_id, link_name, link_phone, link_email, link_address):
        address = Address({
            "user_id": user_id,
            "link_name": link_name,
            "link_phone": link_phone,
            "link_email": link_email,
            "link_address": link_address,
        })
        with session_scope() as session:
            session.add(address)

    def delete_address(self, address_id_list=None):
        if not address_id_list:
            raise Exception("联系人id列表不能为None")
        if not isinstance(address_id_list, list):
            raise Exception("联系人id参数不是一个列表")
        with session_scope() as session:
            address_list = session.query(Address).filter(Address.id.in_(address_id_list))
            for address in address_list:
                address.is_delete = True
                session.add(address)

    def update_address(self, address_id, link_name, link_phone, link_email, link_address):
        with session_scope() as session:
            address = session.query(Address).filter(Address.id == address_id).first()
            address.link_name = link_name
            address.link_phone = link_phone
            address.link_email = link_email
            address.link_address = link_address
            session.add(address)

    def get_address_by_id(self, address_id):
        with session_scope() as session:
            address = session.query(Address).filter(Address.id == address_id).first()
            if not address:
                return None
            return address.to_dict(wanted_list=["id", "user_id", "link_name", "link_phone", "link_email", "link_address", "create_time"])

    def get_all_address_by_page(self, user_id=None, page_size=10, page_now=1):
        with session_scope() as session:
            if not user_id:
                raise Exception("用户ID不能为空")
            elif not check_param_format(param_name=user_id, pattern_list=[r'^[1-9][0-9]*']):
                raise Exception("用户ID格式错误")
            else:
                address_list = session.query(Address).filter(Address.user_id == user_id, Address.is_delete == False).offset((page_now - 1) * page_size).limit(page_size)
            return [address.to_dict(wanted_list=["id", "user_id", "link_name", "link_phone", "link_email", "link_address", "create_time"]) for address in address_list]

    def get_address_by_title_page(self, link_name=None, page_size=10, page_now=1):
        with session_scope() as session:
            if not link_name:
                address_list = session.query(Address).filter(Address.is_delete == False).offset((page_now - 1) * page_size).limit(page_size)
            else:
                address_list = session.query(Address).filter(Address.link_name.like("%{}%".format(link_name)), Address.is_delete == False).offset((page_now - 1) * page_size).limit(page_size)
            return [address.to_dict(wanted_list=["id", "user_id", "link_name", "link_phone", "link_email", "link_address", "create_time"]) for address in address_list]

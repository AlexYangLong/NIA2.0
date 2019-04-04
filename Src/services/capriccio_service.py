# -*- coding: utf-8 -*-
# @author:Alex-PC
# @file: capriccio_service.py
# @time: 2019/03/14

from Src.common.model import Capriccio
from Src.common.service import session_scope
from Src.utils.check_utils import check_param_format


class CapriccioService(object):

    def create_capriccio(self, user_id, extract, content, status, cover):
        capriccio = Capriccio({
            "user_id": user_id,
            "extract": extract,
            "content": content,
            "status": status,
            "cover": cover,
        })
        with session_scope() as session:
            session.add(capriccio)

    def delete_capriccio(self, capriccio_id_list=None):
        if not capriccio_id_list:
            raise Exception("随笔id列表不能为None")
        if not isinstance(capriccio_id_list, list):
            raise Exception("随笔id参数不是一个列表")
        with session_scope() as session:
            capriccio_list = session.query(Capriccio).filter(Capriccio.id.in_(capriccio_id_list))
            for capriccio in capriccio_list:
                capriccio.is_delete = True
                session.add(capriccio)

    def update_capriccio(self, capriccio_id, extract, content, status, cover):
        with session_scope() as session:
            capriccio = session.query(Capriccio).filter(Capriccio.id == capriccio_id).first()
            capriccio.extract = extract
            capriccio.content = content
            capriccio.status = status
            capriccio.cover = cover
            session.add(capriccio)

    def get_capriccio_by_id(self, capriccio_id):
        with session_scope() as session:
            capriccio = session.query(Capriccio).filter(Capriccio.id == capriccio_id).first()
            if not capriccio:
                return None
            return capriccio.to_dict(wanted_list=["id", "user_id", "extract", "content", "status", "zan_times", "cover", "create_time"])

    def get_all_capriccio_by_page(self, user_id=None, page_size=10, page_now=1):
        with session_scope() as session:
            if not user_id:
                capriccio_list = session.query(Capriccio).filter(Capriccio.is_delete == False).offset((page_now - 1) * page_size).limit(page_size)
            elif not check_param_format(param_name=user_id, pattern_list=[r'^[1-9][0-9]*']):
                raise Exception("用户ID格式错误")
            else:
                capriccio_list = session.query(Capriccio).filter(Capriccio.user_id == user_id, Capriccio.is_delete == False).offset((page_now - 1) * page_size).limit(page_size)
            return [capriccio.to_dict(wanted_list=["id", "user_id", "extract", "content", "status", "zan_times", "cover", "create_time"]) for capriccio in capriccio_list]

    def get_capriccio_by_title_page(self, title=None, page_size=10, page_now=1):
        with session_scope() as session:
            if not title:
                capriccio_list = session.query(Capriccio).filter(Capriccio.is_delete == False).offset((page_now - 1) * page_size).limit(page_size)
            else:
                capriccio_list = session.query(Capriccio).filter(Capriccio.title.like("%{}%".format(title)), Capriccio.is_delete == False).offset((page_now - 1) * page_size).limit(page_size)
            return [capriccio.to_dict(wanted_list=["id", "user_id", "extract", "content", "status", "zan_times", "cover", "create_time"]) for capriccio in capriccio_list]



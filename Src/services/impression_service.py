# -*- coding: utf-8 -*-
# @author:Alex-PC
# @file: impression_service.py
# @time: 2019/03/14

from Src.common.model import Impression
from Src.common.service import session_scope


class ImpressionService(object):

    def create_impression(self, user_id, title, abstract, content, status, cover):
        impression = Impression({
            "user_id": user_id,
            "title": title,
            "abstract": abstract,
            "content": content,
            "status": status,
            "cover": cover,
        })
        with session_scope() as session:
            session.add(impression)

    def delete_impression(self, impression_id_list=None):
        if not impression_id_list:
            raise Exception("随笔id列表不能为None")
        if not isinstance(impression_id_list, list):
            raise Exception("随笔id参数不是一个列表")
        with session_scope() as session:
            impression_list = session.query(Impression).filter(Impression.id.in_(impression_id_list))
            for impression in impression_list:
                impression.is_delete = True
                session.add(impression)

    def update_impression(self, impression_id, title, abstract, content, status, cover):
        with session_scope() as session:
            impression = session.query(Impression).filter(Impression.id == impression_id).first()
            impression.title = title
            impression.abstract = abstract
            impression.content = content
            impression.status = status
            impression.cover = cover
            session.add(impression)

    def get_impression_by_id(self, impression_id):
        with session_scope() as session:
            impression = session.query(Impression).filter(Impression.id == impression_id).first()
            if not impression:
                return None
            return impression.to_dict(wanted_list=["id", "user_id", "title", "abstract", "content", "status", "zan_times", "cover", "create_time"])

    def get_all_impression_by_page(self, user_id=None, page_size=10, page_now=1):
        with session_scope() as session:
            if not user_id:
                impression_list = session.query(Impression).filter(Impression.is_delete == False).offset((page_now - 1) * page_size).limit(page_size)
            else:
                impression_list = session.query(Impression).filter(Impression.user_id == user_id, Impression.is_delete == False).offset((page_now - 1) * page_size).limit(page_size)
            return [impression.to_dict(wanted_list=["id", "user_id", "title", "abstract", "content", "status", "zan_times", "cover", "create_time"]) for impression in impression_list]

    def get_impression_by_title_page(self, title=None, page_size=10, page_now=1):
        with session_scope() as session:
            if not title:
                impression_list = session.query(Impression).filter(Impression.is_delete == False).offset((page_now - 1) * page_size).limit(page_size)
            else:
                impression_list = session.query(Impression).filter(Impression.title.like("%{}%".format(title)), Impression.is_delete == False).offset((page_now - 1) * page_size).limit(page_size)
            return [impression.to_dict(wanted_list=["id", "user_id", "title", "abstract", "content", "status", "zan_times", "cover", "create_time"]) for impression in impression_list]



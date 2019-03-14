# -*- coding: utf-8 -*-
# @author:Alex-PC
# @file: diary_service.py
# @time: 2019/03/14

from Src.common.model import Diary
from Src.common.service import session_scope


class DiaryService(object):

    def create_diary(self, user_id, week, weather, mood, content, status, cover):
        diary = Diary({
            "user_id": user_id,
            "week": week,
            "weather": weather,
            "mood": mood,
            "content": content,
            "status": status,
            "cover": cover,
        })
        with session_scope() as session:
            session.add(diary)

    def delete_diary(self, diary_id_list=None):
        if not diary_id_list:
            raise Exception("随笔id列表不能为None")
        if not isinstance(diary_id_list, list):
            raise Exception("随笔id参数不是一个列表")
        with session_scope() as session:
            diary_list = session.query(Diary).filter(Diary.id.in_(diary_id_list))
            for diary in diary_list:
                diary.is_delete = True
                session.add(diary)

    def update_diary(self, diary_id, week, weather, mood, content, status, cover):
        with session_scope() as session:
            diary = session.query(Diary).filter(Diary.id == diary_id).first()
            diary.week = week
            diary.weather = weather
            diary.mood = mood
            diary.content = content
            diary.status = status
            diary.cover = cover
            session.add(diary)

    def get_diary_by_id(self, diary_id):
        with session_scope() as session:
            diary = session.query(Diary).filter(Diary.id == diary_id).first()
            if not diary:
                return None
            return diary.to_dict(wanted_list=["id", "user_id", "week", "weather", "mood", "content", "status", "zan_times", "cover", "create_time"])

    def get_all_diary(self, user_id=None):
        with session_scope() as session:
            if not user_id:
                diary_list = session.query(Diary).filter(Diary.is_delete == False)
            else:
                diary_list = session.query(Diary).filter(Diary.user_id == user_id, Diary.is_delete == False)
            return [diary.to_dict(wanted_list=["id", "user_id", "week", "weather", "mood", "content", "status", "zan_times", "cover", "create_time"]) for diary in diary_list]

    def get_diary_by_title(self, title=None):
        with session_scope() as session:
            if not title:
                diary_list = session.query(Diary).filter(Diary.is_delete == False)
            else:
                diary_list = session.query(Diary).filter(Diary.content.like("%{}%".format(title)), Diary.is_delete == False)
            return [diary.to_dict(wanted_list=["id", "user_id", "week", "weather", "mood", "content", "status", "zan_times", "cover", "create_time"]) for diary in diary_list]



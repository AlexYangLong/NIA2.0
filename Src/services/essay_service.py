from Src.common.model import Essay
from Src.common.service import session_scope
from Src.utils.check_utils import check_param_format


class EssayService(object):

    def create_essay(self, user_id, title, abstract, content, status, cover):
        essay = Essay({
            "user_id": user_id,
            "title": title,
            "abstract": abstract,
            "content": content,
            "status": status,
            "cover": cover,
        })
        with session_scope() as session:
            session.add(essay)

    def delete_essay(self, essay_id_list=None):
        if not essay_id_list:
            raise Exception("随笔id列表不能为None")
        if not isinstance(essay_id_list, list):
            raise Exception("随笔id参数不是一个列表")
        with session_scope() as session:
            essay_list = session.query(Essay).filter(Essay.id.in_(essay_id_list))
            for essay in essay_list:
                essay.is_delete = True
                session.add(essay)

    def update_essay(self, essay_id, title, abstract, content, status, cover):
        with session_scope() as session:
            essay = session.query(Essay).filter(Essay.id == essay_id).first()
            essay.title = title
            essay.abstract = abstract
            essay.content = content
            essay.status = status
            essay.cover = cover
            session.add(essay)

    def get_essay_by_id(self, essay_id):
        with session_scope() as session:
            essay = session.query(Essay).filter(Essay.id == essay_id).first()
            if not essay:
                return None
            return essay.to_dict(wanted_list=["id", "user_id", "title", "abstract", "content", "status", "zan_times", "cover", "create_time"])

    def get_all_essay_by_page(self, user_id=None, page_size=10, page_now=1):
        with session_scope() as session:
            if not user_id:
                essay_list = session.query(Essay).filter(Essay.is_delete == False).offset((page_now - 1) * page_size).limit(page_size)
            elif not check_param_format(param_name=user_id, pattern_list=[r'^[1-9][0-9]*']):
                raise Exception("用户ID格式错误")
            else:
                essay_list = session.query(Essay).filter(Essay.user_id == user_id, Essay.is_delete == False).offset((page_now - 1) * page_size).limit(page_size)
            return [essay.to_dict(wanted_list=["id", "user_id", "title", "abstract", "content", "status", "zan_times", "cover", "create_time"]) for essay in essay_list]

    def get_essay_by_title_page(self, title=None, page_size=10, page_now=1):
        with session_scope() as session:
            if not title:
                essay_list = session.query(Essay).filter(Essay.is_delete == False).offset((page_now - 1) * page_size).limit(page_size)
            else:
                essay_list = session.query(Essay).filter(Essay.title.like("%{}%".format(title)), Essay.is_delete == False).offset((page_now - 1) * page_size).limit(page_size)
            return [essay.to_dict(wanted_list=["id", "user_id", "title", "abstract", "content", "status", "zan_times", "cover", "create_time"]) for essay in essay_list]




"""
    字典表通用sql
"""
from system.models import Project_dict, Title_url_model


class Dict_mapper:

    @staticmethod
    def query_by_type(type):
        """
            根据类型查询对象
        :param type: 类型
        :return:
        """
        return Project_dict.objects.filter(type=type)
    
    
class Title_url_mapper:
    @staticmethod
    def query_box(type):
        re = Title_url_model.objects.values_list("title", "url").filter(type=type).order_by("sort")
        return {item[0]: item[1] for item in re}

    @staticmethod
    def query_title_by_type(type):
        re = Title_url_model.objects.filter(Title_url_model.title, Title_url_model.url, Title_url_model.parent_id).filter(
            Title_url_model .type == type) \
            .order_by(Title_url_model.sort)
        childs = {item[0]: item[1] for item in re if item[2] != 0}
        return childs












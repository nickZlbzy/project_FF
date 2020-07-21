"""
    字典表通用sql
"""
from base.core.LinkedList import linkedList
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

    @staticmethod
    def query_title_by_module(module):
        re = Title_url_model.objects.values('id','title', 'url', 'parent_id', 'type').filter(
            module=module).order_by('parent_id','sort')
        # 为提升性能转化为链表
        list_re = linkedList(tuple(re))
        re_dic = {}
        for item in list_re:
            if item.get('parent_id') == 0:
                # print(list_re.length())
                dic = {}
                dic["type"] = item.get('type')
                dic["title"] = item.get('title')
                dic["url"] = item.get('url')
                dic["id"] = item.get('id')
                list_re.remove(item)
                Title_url_mapper.add_child(dic, list_re)
                re_dic[item.get("type")] = dic
        re_dic = re_dic if re_dic else ""
        return re_dic

    @staticmethod
    def add_child(dic, l_data):
        for l_item in l_data:
            if l_item.get('parent_id') == dic.get("id"):
                if not dic.get("childs"):
                    dic["childs"] = []
                dic_son = {}
                dic_son["type"] = l_item.get('type')
                dic_son["title"] = l_item.get('title')
                dic_son["url"] = l_item.get('url')
                dic_son["parent_id"] = l_item.get('parent_id')
                dic["childs"].append(dic_son)
                l_data.remove(l_item)

















import json

from django.db.models import F

from article.models import *
from base.core.LinkedList import *



class Article_mapper:
    @staticmethod
    def select_by_artId(article_id):
        data = Article_info_model.objects.values('title','author','update_time','content','level_id'
                ).filter(article_id=article_id)[0]
        return data

    @staticmethod
    def get_title_by_lid(level_id):
        re = Article_level_model.objects.values('title','url').filter(lid=level_id,parent_id="0")

        return re[0] if re else ""

    @staticmethod
    def select_course_by_artId(article_id):
        data = Article_info_model.objects.values('title' , 'content', 'next','next_url'
                                            ).filter(article_id=article_id)[0]
        return data

    @staticmethod
    def query_article_parent():
        re = Article_level_model.objects.values('url', 'title','lid').filter(parent_id="0",
              module="article_info").order_by("sort")
        return re if re else ""

    @staticmethod
    def query_title_by_name(value):
        sql = "select article_id,url,title from t_article_info where is_active = 1 and " \
              "instr(title,'%s')=1" % value
        re = Article_info_model.objects.raw(sql)
        # 返回了rawQuerySet生成器对象，这里用字典生成式处理
        return {item.url:item.title for item in re} if re else ""

    @staticmethod
    def query_by_kind(kind,pagesize=10):
        re = Article_level_model.objects.filter(module=kind).order_by('sort')


        return {item.kind:{"title":item.title,"childs":item.info.all()[:pagesize]} for item in re} if re else ""




    # @staticmethod
    # def query_by_type(type,pagesize=10):
    #     re = Article_model.objects.values('title', 'url', 'parent_id','article_id','article_type').filter(
    #         level_id=type).order_by('sort')[:pagesize]
    #     # 提升方法迭代性能转化为链表
    #     list_re = linkedList(tuple(re))
    #     re_dic = {}
    #     for item in list_re:
    #         if item.get('parent_id') == "0":
    #             # print(list_re.length())
    #             dic = {}
    #             dic["art_id"] = item.get('article_id')
    #             dic["title"] = item.get('title')
    #             dic["url"] = item.get('url')
    #             dic["parent_id"] = item.get('parent_id')
    #             list_re.remove(item)
    #             # for item2 in list_re:
    #             Article_mapper.create_child(dic, list_re)
    #             re_dic[item.get("article_type")] = dic
    #     re_dic = re_dic if re_dic else ""
    #     return re_dic
    #
    # @staticmethod
    # def create_child(dic ,l_data):
    #     for l_item in l_data:
    #         if l_item.get('parent_id') == dic.get("art_id"):
    #             if not dic.get("childs"):
    #                 dic["childs"] = []
    #             dic_son = {}
    #             dic_son["art_id"] = l_item.get('article_id')
    #             dic_son["title"] = l_item.get('title')
    #             dic_son["url"] = l_item.get('url')
    #             dic_son["parent_id"] = l_item.get('parent_id')
    #             dic["childs"].append(dic_son)
    #             l_data.remove(l_item)
    #             for item in l_data:
    #                 Article_mapper.create_child(dic_son, l_data)

    @staticmethod
    def query_article_list2(type,module=None):
        if module:
            re = Article_level_model.objects.filter(module=module, kind=type)
        else:
            re = Article_level_model.objects.filter(kind=type)

        # 提升方法迭代性能转化为链表
        list_re = linkedList(tuple(re))
        re_dic = {}
        for item in list_re:
            if item.parent_id == "0":
                # print(list_re.length())
                dic = {}
                dic["lid"] = item.lid
                dic["title"] = item.title
                dic["url"] = item.url
                dic["parent_id"] = item.parent_id
                list_re.remove(item)
                # for item2 in list_re:
                Article_mapper.create_cls_child(dic, list_re)
                re_dic[item.lid] = dic

        return re_dic

    @staticmethod
    def query_cls_all(level_id=None):
        """

        :param level_id:
        :return: re_dic  右侧列表   re_list 左侧标题
        """
        re = Article_level_model.objects.filter(module='inv_course',kind='cls')

        # 提升方法迭代性能转化为链表
        list_re = linkedList(tuple(re))
        re_dic,re_list = {},None
        for item in list_re:
            if not level_id and not re_list:
                re_list = item.info.all()
            elif level_id and item.lid == level_id:
                re_list = item.info.all()
            if item.parent_id == "0":
                # print(list_re.length())
                dic = {}
                dic["lid"] = item.lid
                dic["title"] = item.title
                dic["url"] = item.url

                dic["parent_id"] = item.parent_id
                list_re.remove(item)
                # for item2 in list_re:
                Article_mapper.create_cls_child(dic, list_re)
                re_dic[item.lid] = dic

        return re_dic,re_list

    @staticmethod
    def create_cls_child(dic, l_data):
        for l_item in l_data:
            if l_item.parent_id == dic.get('lid'):
                if not dic.get("childs"):
                    dic["childs"] = []
                dic_son = {}
                dic_son["lid"] = l_item.lid
                dic_son["title"] = l_item.title
                dic_son["url"] = l_item.url
                dic_son["parent_id"] = l_item.parent_id
                dic["childs"].append(dic_son)
                l_data.remove(l_item)
                for item in l_data:
                    Article_mapper.create_cls_child(dic_son, l_data)

    @staticmethod
    def query_type_article(level_id):
        re = Article_info_model.objects.values("title", "url", "author", "update_time").filter(
            level_id = level_id).order_by("sort")
        re_list = []
        for item in re:
            dic = {}
            dic["title"] = item.get("title")
            dic["url"] = item.get("url")
            dic["author"] = item.get("author")
            dic["op_date"] = item.get("update_time")
            re_list.append(dic)
        return re_list






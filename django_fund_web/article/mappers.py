from django.db.models import F

from article.models import Article_model
from base.core.LinkedList import *



class Article_mapper:
    @staticmethod
    def query_by_artId(article_id):
        data = Article_model.objects.values('title','author','update_time','content','article_type'
                ).filter(article_id=article_id)[0]
        return data

    @staticmethod
    def get_title_by_type(type):
        re = Article_model.objects.values('title').filter(article_type=type,parent_id="0")

        return re[0].get("title") if re else ""

    @staticmethod
    def query_article_parent():
        re = Article_model.objects.values_list('url', 'title').filter(parent_id="0",
              module_type="art_info").order_by("sort")
        return dict(re) if re else ""

    @staticmethod
    def query_title_by_name(value):
        sql = "select url,title from t_article where parent_id != '0' and locate('%s',title)" % value
        re = Article_model.objects.raw(sql)
        return dict(re) if re else ""

    @staticmethod
    def query_by_type(type,pagesize=10):
        re = Article_model.objects.values('title', 'url', 'parent_id','article_id','article_type').filter(
            module_type=type).order_by('sort')[:pagesize]
        # 为提升性能转化为链表
        list_re = linkedList(tuple(re))
        re_dic = {}
        for item in list_re:
            if item.get('parent_id') == "0":
                # print(list_re.length())
                dic = {}
                dic["art_id"] = item.get('article_id')
                dic["title"] = item.get('title')
                dic["url"] = item.get('url')
                dic["parent_id"] = item.get('parent_id')
                list_re.remove(item)
                for item2 in list_re:
                    Article_mapper.create_child(dic, item2, list_re)
                re_dic[item.get("article_type")] = dic
        re_dic = re_dic if re_dic else ""
        return re_dic

    @staticmethod
    def create_child(dic, l_item, l_data):
        if l_item.get('parent_id') == dic.get("art_id"):
            if not dic.get("childs"):
                dic["childs"] = []
            dic_son = {}
            dic_son["art_id"] = l_item.get('article_id')
            dic_son["title"] = l_item.get('title')
            dic_son["url"] = l_item.get('url')
            dic_son["parent_id"] = l_item.get('parent_id')
            dic["childs"].append(dic_son)
            l_data.remove(l_item)
            for item in l_data:
                Article_mapper.create_child(dic_son, item, l_data)


    @staticmethod
    def query_type_article(type):
        re = Article_model.objects.values("title", "url", "author", "update_time").filter(
            article_type = type).exclude(parent_id=0).order_by("sort")
        re_list = []
        for item in re:
            dic = {}
            dic["title"] = item.get("title")
            dic["url"] = item.get("url")
            dic["author"] = item.get("author")
            dic["op_date"] = item.get("update_time")
            re_list.append(dic)
        return re_list






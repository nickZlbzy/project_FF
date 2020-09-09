from django.forms import model_to_dict

from base.core.LinkedList import linkedList
from post.models import *
from user.mappers import User_mapper


class Post_mapper:

    @staticmethod
    def query_home_titles():
        re = Post_title_model.objects.values('comment_count','theme','author',
                    'create_time','update_time','url','bar_id', 't_sort').all()

        re_list = []
        bar_dic = {}
        for item in re:
            dic = {}
            dic["bar_id"] = item.get("bar_id")
            if bar_dic and bar_dic.get(dic["bar_id"]):
                dic["parent_bar"] = parent_bar
            else:
                try:
                    parent_bar = Post_bar_model.objects.values('name', 'url').get(bid=dic["bar_id"])
                except Exception as e:
                    print(e)
                    continue
                bar_dic[item.get("bar_id")] = parent_bar
                dic["parent_bar"] = parent_bar
            dic["theme"] = item.get("theme")
            dic["url"] = item.get("url")
            dic["author"] = item.get("author")
            dic["create_time"] = item.get("create_time")
            dic["update_time"] = item.get("update_time")
            dic["comment_count"] = item.get("comment_count")
            dic["top_sort"] = item.get("t_sort")
            re_list.append(dic)
        return re_list

    @staticmethod
    def query_bar_titles(b_id,sort_pub=0):
        """

        :param b_id:
        :param sort_pub: 0 评论排序/ 1 发布排序
        :return:
        """
        if sort_pub:
            re = Post_title_model.objects.values('comment_count', 'theme', 'author',
                     'create_time', 'update_time', 'url', 't_sort').filter(bar_id=b_id).order_by(
                '-t_sort','-create_time').all()
        else:
            re = Post_title_model.objects.values('comment_count', 'theme', 'author',
                     'create_time', 'update_time', 'url').filter(bar_id=b_id).all()
        re_list = []
        for item in re:
            dic = {}
            dic["theme"] = item.get("theme")
            dic["url"] = item.get("url")
            dic["author"] = item.get("author")
            dic["create_time"] = item.get("create_time")
            dic["update_time"] = item.get("update_time")
            dic["comment_count"] = item.get("comment_count")
            dic["top_sort"] = item.get("t_sort")
            re_list.append(dic)
        return re_list

    @staticmethod
    def get_theme_info(t_id):
        re = Post_title_model.objects.filter(tid=t_id)[0]
        theme_info = model_to_dict(re)
        userinfo= User_mapper.get_user_info(re.author)
        theme_info['nickname'] = userinfo.get('nickname')
        theme_info['userimg'] = userinfo.get('userimg')
        theme_info['userurl'] = userinfo.get('userurl')
        theme_info['c_time']= re.create_time.strftime("%Y-%m-%d %H:%M:%S")
        theme_info['b_name']= re.bar.name
        theme_info['b_url']= re.bar.url
        theme_info['b_fund_code']= re.bar.fund_code
        theme_info['b_count']= re.bar.post_count
        return theme_info

    @staticmethod
    def query_theme_comments(t_id):
        re = Post_comment_model.objects.values('id', 'author', 'content', 'parent_id',
               'revert_to', 'sort', 'create_time').filter(theme_id=t_id).all()
        # 提升方法迭代效率转化为链表
        list_re = linkedList(tuple(re))
        list_comment = [];user_dic = {}
        for item in list_re:
            if item.get('parent_id') == 0:
                dic = {}
                dic['id'] = item.get('id')
                dic['content'] = item.get('content')
                dic['create_time'] = item.get('create_time')
                dic['author'] = item.get('author')
                dic['sort'] = item.get('sort')
                # 实际用缓存实现
                if not dic['author'] in user_dic:
                    user_dic[dic['author']] = User_mapper.get_user_info(item.get('author'))

                dic['nickname'] = user_dic[dic['author']]['nickname']
                dic['userimg'] = user_dic[dic['author']]['userimg']
                dic['userurl'] = user_dic[dic['author']]['userurl']

                list_comment.append(dic)
                list_re.remove(item)

        for item in list_comment:
            Post_mapper.add_comment_childs(item,list_re,user_dic)

        return list_comment

    @staticmethod
    def add_comment_childs(dic,l_data,user_dic):
        for item in l_data:
            if dic['id'] == item['parent_id']:
                if not dic.get("childs"):
                    dic["childs"] = []
                dic_son = {}
                dic_son['id'] = item.get('id')
                dic_son['content'] = item.get('content')
                dic_son['create_time'] = item.get('create_time')
                dic_son['author'] = item.get('author')
                dic_son['parent_id'] = item.get('parent_id')
                if not dic_son['author'] in user_dic:
                    user_dic[dic_son['author']] = User_mapper.get_user_info(item.get('author'))
                dic_son['nickname'] = user_dic[dic_son['author']]['nickname']
                dic_son['userimg'] = user_dic[dic_son['author']]['userimg']
                dic_son['userurl'] = user_dic[dic_son['author']]['userurl']
                if item.get("revert_to"):
                    if not item.get("revert_to") in user_dic:
                        user_dic[dic_son['revert_to']] = User_mapper.get_user_info(item.get('revert_to'))
                    dic_son['revert_to'] = item.get("revert_to")
                    dic_son['revert_name'] = user_dic.get(item.get('revert_to')).get('nickname')
                    dic_son['revert_userurl'] = user_dic[dic['author']]['userurl']
                dic['childs'].append(dic_son)
                l_data.remove(item)




## Old_code

1.  (old) Query_by

```python
    @staticmethod
    def query_by_type(type,pagesize=10):
        re = Article_model.objects.values('title', 'url', 'parent_id','article_id','article_type').filter(
            level_id=type).order_by('sort')[:pagesize]
        # 提升方法迭代性能转化为链表
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
                # for item2 in list_re:
                Article_mapper.create_child(dic, list_re)
                re_dic[item.get("article_type")] = dic
        re_dic = re_dic if re_dic else ""
        return re_dic

    @staticmethod
    def create_child(dic ,l_data):
        for l_item in l_data:
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
                    Article_mapper.create_child(dic_son, l_data)
```

2. Hot_bars

   ```python
   def query_hot_bar(request,count):
       print(type(count))
       list_bar = Post_bar_model.objects.values('name','url').all()[:int(count)]
       print(list_bar)
       re_data = {'code':200,
                  'data':[{'url':item.get('url'),'name':item.get('name')} for item in list_bar]}
       return JsonResponse(re_data)
   ```

   
from article.models import Article_model,Article_level_model
from base.core.LinkedList import *


def make_cls_ok():
    """
    投资学堂数据处理
    :return:
    """
    next_queue = []
    re = Article_level_model.objects.filter(module='inv_course', kind='cls')
    for item1 in re:
        if item1.parent_id != 0:
            for item2 in item1.article_info_model_set.all():
                if not item2.url.startswith('/article/course'):
                    o_url = item2.url
                    item2.url = '/article/course' + o_url
                    item2.save()
                next_queue.append((item2.url,item2.title))
    # 去掉第一个文章的url
    next_queue = next_queue[1:]

    list_re = linkedList(tuple(re))
    for item in list_re:
        if item.parent_id == "0":
            list_re.remove(item)
            list_re.travel()
            for n1, i1 in enumerate(list_re):
                if i1.parent_id == item.lid:
                    list_re.remove(i1)
                    print(i1.title)
                    for n2, i2 in enumerate(i1.article_info_model_set.all()):
                        if len(next_queue) > 0:
                            next_one = next_queue.pop(0)
                            i2.next_url = next_one[0]
                            i2.next = next_one[1]
                            i2.save()
                        if n2 == 0:
                            i1.url = i2.url
                            i1.save()
                            if n1 == 0:
                                item.url = i2.url
                                item.save()
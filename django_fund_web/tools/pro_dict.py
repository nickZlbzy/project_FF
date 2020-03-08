"""
    项目字典
    存放常用的valid与中文名称的映射
"""
from django_redis import get_redis_connection

from system.models import Project_dict

r = get_redis_connection('project_dict')
# 支付状态
# PAYMENT_STATUS={
#     1:"待付款",
#     2:"已支付",
#     3:"已完成",
#     4:"已取消",
# }

def get_from_dict(type,valid,default_re=""):
    """
    从字典中获取
    :param type:    类型
    :param valid:   再此类中的id
    :return:
    """
    result = r.hget(type,valid)

    if result:
        return result.decode()
    print('=' * 45)
    print('加载缓存')
    dicts = {}
    querySet = Project_dict.objects.values('type','valid','value').all()
    for item in querySet:
        type = item['type']
        valid = item['valid']
        value = item['value']
        if type not in dicts.keys():
            dicts[type]={}
        dicts[type][valid] = value
    for key in dicts.keys():
        r.hmset(key,dicts[key])

    if type in dicts:
        return dicts[type].get(valid,"")
    return default_re






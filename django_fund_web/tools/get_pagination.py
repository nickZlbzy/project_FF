import math

from django.core.paginator import Paginator

from tools.contants import DEFAULT_MAX_PAGE

def get_pagination(list_data,pageNum,pageSize=25):
    """
    自定义分页功能
    :param list_data:   数据列表
    :param pageNum:     页数
    :param pageSize:    每页显示最大数量
    :return:        (pages,data)  页面导航对象， 分页的数据。
    """
    pagination = Paginator(list_data, pageSize)
    page = pagination.page(pageNum)
    paging = {}
    paging['next_num'] = page.next_page_number() if page.has_next() else 0
    paging['prev_num'] = page.previous_page_number() if page.has_previous() else 0
    paging['number'] = page.number
    paging['page_size'] = pagination.per_page
    # 需要把pages对象转为列表
    rows = list(pagination.page_range)
    index = 0
    while rows:
        index += 1
        row = rows[:DEFAULT_MAX_PAGE]
        if page.number in row:
            paging['page_range'] = row
            break;
        rows = rows[DEFAULT_MAX_PAGE:]
    else:
        paging['page_range'] = None
    paging['page_count'] = pagination.num_pages
    length = math.ceil(pagination.num_pages / DEFAULT_MAX_PAGE)
    if index == 1:
        paging['next_range_num'] = index * DEFAULT_MAX_PAGE + 1
    elif index == length:
        paging['prev_range_num'] = (index - 1) * DEFAULT_MAX_PAGE
    else:
        paging['next_range_num'] = index * DEFAULT_MAX_PAGE + 1
        paging['prev_range_num'] = (index - 1) * DEFAULT_MAX_PAGE
    return paging,page.object_list
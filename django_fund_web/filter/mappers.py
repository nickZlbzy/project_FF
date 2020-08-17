from django.db import connection
from django.db.models import Manager

from filter.models import Fund_filter_model, Fund_type, Fund_company


class Fund_filter_mapper:
    # 基金筛选器所需的字段信息
    sql_base = "select id,f_code,f_name,three_year_level,five_year_level,interest,unit_price,day_change, " \
               "update_time, " \
               "(select a.c_name from t_fund_company a where a.c_id=company_id)," \
               "(select b.value from system_dict b where b.valid=is_oc and b.type='oc_sel')," \
               "(select c.value from system_dict c where c.valid=is_eq and c.type='eq_sel')," \
               "(select d.type_name as type_name from t_fund_type d where d.t_id=f_type_id) " \
               "from t_fund_filter as t1"

    @staticmethod
    def query_list(page=1, *, f_name=None, is_oc=0, is_eq=[], company_id=None, f_type=[],
                   three_year_level=0, five_year_level=0, page_size=25):
        """
            分页查询方法
        :param page:        页码
        :param page_size:   每页显示的记录数量
        :return:
        """
        # 使用 exists的方式优化 in 查询语句
        re_sql = " WHERE EXISTS (SELECT id FROM t_fund_filter t2 WHERE t2.id=t1.id"
        if f_name:
            re_sql += " AND instr(t2.f_name,'%s') > 0"% f_name
        if is_oc:
            re_sql += " AND t2.is_oc=%s" % is_oc
        if is_eq:  # in (1,2)语句处理方法
            re_sql += Fund_filter_mapper.get_sql_set(is_eq, "t2.is_eq")
        if f_type:
            re_sql += Fund_filter_mapper.get_sql_set(f_type, "t2.f_type_id")
        if company_id:
            re_sql += " AND t2.company_id=%s" % company_id
        # 三年/五年评级
        if three_year_level == "1":
            re_sql += " AND t2.three_year_level>=3"
        elif three_year_level == "2":
            re_sql += " AND t2.three_year_level>0 AND three_year_level<3"
        if five_year_level == "1":
            re_sql += " AND t2.five_year_level>=3"
        elif five_year_level == "2":
            re_sql += " AND t2.five_year_level>0 AND five_year_level<3"

        re_sql += " )"
                  # "limit %d,%d" % (page_size * (page - 1), page_size)

        sql = Fund_filter_mapper.sql_base + re_sql
        with connection.cursor() as cursor:
            cursor.execute(sql)
            re = cursor.fetchall()

        return Fund_filter_mapper.change_dict(re)

    @staticmethod
    def get_sql_set(param, str_column):
        """
            得到集合元素的sql
        :param param:      参数对象
        :param str_column: 字段名
        :return:
        """
        if type(param) == int or len(param) == 1:
            re_str = " AND %s=%s" % (str_column, param[0])
            return re_str
        else:
            str_set = ""
            for i in range(len(param)):
                if i:  # 如果不是第一个元素,拼一个 ,
                    str_set += ","
                str_set += str(param[i])

            sql_set = "(" + str_set + ")"
            return " AND %s in " % str_column + sql_set

    list = ["★", "✩"]

    @classmethod
    def get_star(cls, num):
        re_str = cls.list[1] * 5
        return re_str.replace(cls.list[1], cls.list[0], int(num))

    @staticmethod
    def change_dict(list_fund_filter):
        """
            将查询结果转为用户看到的数据
        :param list_fund_filter:
        :return: dict
        """
        re_list = []

        if list_fund_filter:
            for item in list_fund_filter:
                fund_dict = {}
                fund_dict["id"] = item[0]
                fund_dict["f_code"] = item[1]
                fund_dict["f_name"] = item[2]
                fund_dict["three_year_level"] = Fund_filter_mapper.get_star(item[3])
                fund_dict["five_year_level"] = Fund_filter_mapper.get_star(item[4])
                fund_dict["interest"] = float(item[5])
                fund_dict["unit_price"] = item[6]
                fund_dict["day_change"] = float(item[7])
                fund_dict["update_time"] = item[8]
                fund_dict["company_name"] = item[9]
                fund_dict["oc_name"] = item[10]
                fund_dict["eq_name"] = item[11]
                fund_dict["type_name"] = item[12]
                re_list.append(fund_dict)
        return re_list

    @staticmethod
    def select_wonder_fund():
        sql = "select f_code, f_name, " \
              "(select a.type_name from t_fund_type a where a.t_id=f_type_id) as t_name " \
              "from t_fund_filter order by interest desc limit 1,15"

        with connection.cursor() as cursor:
            cursor.execute(sql)
            re = cursor.fetchall()
        re_list = []
        if re:
            for item in re:
                fund_dict = {}
                fund_dict["f_code"] = item[0]
                fund_dict["f_name"] = item[1]
                fund_dict["type_name"] = item[2]
                re_list.append(fund_dict)
        return re_list

    @staticmethod
    def select_fund_by_code(code):
        try:
            fund_info = Fund_filter_model.objects.get(is_active=1,f_code=code)
        except:
            return 0
        return fund_info



class Fund_type_mapper:
    @staticmethod
    def get_valid_by_name(type_name):
        # re = db.session().query(fund_type.t_id).fund_filter(fund_type.type_name==type_name).first()
        sql = "select t_id from t_fund_type where locate(type_name,'%s')" % type_name
        re = Fund_type.objects.execute(sql)
        if re:
            return re[0]
        return 20

class Fund_company_mapper:

    @staticmethod
    def query_box():
        list_company = Fund_company.objects.values_list('c_id', 'c_name').all()
        return {item[0]: item[1] for item in list_company}
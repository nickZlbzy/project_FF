import hashlib

from django.conf import settings


class Utils:

    @staticmethod
    def make_md5s(pwd):
        """
            密码md5加密
        :param pwd:
        :return:
        """
        md5 = hashlib.md5()
        md5.update(pwd.encode())
        md5.update(settings.SECRET_SALT.encode())
        return md5.hexdigest()
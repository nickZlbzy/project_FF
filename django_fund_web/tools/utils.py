import hashlib
from threading import Lock

from django.conf import settings
from django.db.models import F

from system.models import Sync_code


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

    @staticmethod
    def get_sync(module_name):
        lock = Lock()
        code = ""
        try:
            lock.acquire()
            sync_code =  Sync_code.objects.filter(module=module_name)[0]
            code = sync_code.prefix + str(sync_code.serial_num)
            sync_code.serial_num = sync_code.serial_num+1
            sync_code.save()
            lock.release()
        except Exception as e:
            lock.release()
            return ""
        return code



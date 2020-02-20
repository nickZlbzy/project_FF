from django.db import models


class BaseModel(models.Model):
    """
        项目基类
    """
    create_time = models.DateField(auto_now_add=True)
    update_time = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=1)
    remarks = models.CharField(max_length=50,default="", blank=True)

    class Meta:
        abstract = True

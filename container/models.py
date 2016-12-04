from django.db import models
from worker.models import Partment
from . import STATUS
# Create your models here.

class Car(models.Model):
    license = models.CharField('车牌号',primary_key=True,max_length=15)
    status = models.CharField('状态',choices=STATUS,default="relaxing",max_length=10)
    def __str__(self):
        return self.license
    class Meta:
        verbose_name = '押款车'
        verbose_name_plural = '押款车'

class Container(models.Model):
    number = models.CharField('编号',max_length=20,primary_key=True)
    partment = models.ForeignKey(Partment,verbose_name="所属部门")
    location = models.CharField("箱子所在地",max_length=20)
    status = models.CharField('状态',choices=STATUS,default="relaxing",max_length=20)
    def __str__(self):
        return self.number
    class Meta:
        verbose_name = '货箱'
        verbose_name_plural = '货箱'



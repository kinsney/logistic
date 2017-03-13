from django.db import models
from worker.models import Partment
from . import STATUS,GUN_STATUS
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
        return '{}-{}'.format(self.number,self.partment)
    class Meta:
        verbose_name = '货箱'
        verbose_name_plural = '货箱'

class GunType(models.Model):
    name = models.CharField('枪支型号',max_length=20)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '枪支型号'
        verbose_name_plural = '枪支型号'

class Bullet(models.Model):
    type = models.CharField('子弹类型',max_length=10)
    number = models.SmallIntegerField('子弹数量',default=0)
    class Meta:
        verbose_name = '子弹'

class Gun(models.Model):
    number = models.CharField('标签编号',max_length=20,primary_key=True)
    gunNumber = models.CharField('枪支编号',max_length=20)
    type = models.ForeignKey(GunType,verbose_name="枪支型号")
    prof = models.CharField('枪证号',max_length=20)
    status = models.CharField('状态',choices=GUN_STATUS,default="relaxing",max_length=20)
    def __str__(self):
        return '编号为{}的{}'.format(self.number,self.type)
    class Meta:
        verbose_name = '枪支'
        verbose_name_plural = '枪支'

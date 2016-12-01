from django.db import models
from django.contrib.auth.models import User
from worker.validators import IdCardValidator
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey
from . import STATUS,PROFILE
import datetime
# Create your models here.
#
class Partment(MPTTModel):
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        verbose_name='上级部门'
    )
    location = models.CharField('位置', max_length=30,blank=True)
    name = models.CharField('名称', max_length=20,blank=False)
    def has_child(self, child):
        return child.lft > self.lft and child.rght < self.rght
    def __str__(self):
        if self.parent:
            return "{}{}".format(self.parent,self.name)
        else :
            return self.name
    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门'

class Worker(models.Model):
    user = models.OneToOneField(User, verbose_name='用户', primary_key=True)
    personId = models.CharField('身份证号', max_length=18, validators=[IdCardValidator()], blank=True)
    avatar = models.ImageField('头像',blank=True)
    workerId = models.CharField('工号',max_length=20,blank=True)
    name = models.CharField('姓名',max_length=10,blank=True)
    partment = models.ForeignKey(
        Partment,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="所属部门"
        )
    status = models.CharField('工作状态',choices=STATUS,default='working',max_length=20)
    profile = models.CharField('身份',max_length=10,choices=PROFILE)
    def __str__(self):
        mapping ={"guarder":'押解员',
                 'watcher':'仓库管理员',
                 "driver":"司机",
                 "banker":"银行验收员"
                    }
        return "{}-{}".format(mapping[self.profile],self.name)
    def phone(self):
        return self.user.username
    def get_today_mission(self):
        today = datetime.date.today()
        # return self.mission_set.filter(time_start__day=today.day,time_start__month=today.month,time_start__year=today.year)
        return self.mission_set.all()
    class Meta:
        verbose_name = '工作人员'
        verbose_name_plural = '工作人员'



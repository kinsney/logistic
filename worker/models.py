from django.db import models
from django.contrib.auth.models import User
from worker.validators import IdCardValidator
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models import Q
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
            return "{}-{}".format(self.parent,self.name)
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
        mapping ={"guarder":'押送员',
                 'watcher':'仓库管理员',
                 "driver":"司机",
                 "banker":"银行验收员",
                 "reliver":"解款员",
                 "keeper":"枪支管理员"
                    }
        return "{}-{}".format(mapping[self.profile],self.name)
    def phone(self):
        return self.user.username
    def get_today_mission(self):
        today = datetime.date.today()
        readyTodayMission = self.mission_set.model.objects.filter(template=False,time_start__day=today.day,time_start__month=today.month,time_start__year=today.year)
        if readyTodayMission.count() == 0:
            todayMissionTemplate = self.mission_set.model.objects.filter(template=True).filter(Q(time_start__lte = today)|Q(time_start__day=today.day,time_start__month=today.month,time_start__year=today.year))
            templateMissionPk = 0
            for m in todayMissionTemplate:
                templateMissionPk = m.pk
                m.pk = None
                m.save()
                m.template = False
                templateMission = self.mission_set.model.objects.get(pk=templateMissionPk)
                m.worker.add(*templateMission.worker.all())
                m.guns.add(*templateMission.guns.all())
                m.time_start = m.time_start.replace(year = today.year, month = today.month, day = today.day)
                m.time_end = m.time_end.replace(year = today.year, month = today.month, day = today.day)
                m.save()
                templateTaskPk = 0
                for t in templateMission.task_set.all():
                    templateTaskPk = t.pk
                    t.pk = None
                    t.save()
                    templateTask = templateMission.task_set.model.objects.get(pk=templateTaskPk)
                    t.load_container.add(*templateTask.load_container.all())
                    t.unload_container.add(*templateTask.unload_container.all())
                    t.mission_time = t.mission_time.replace(year = today.year, month = today.month, day = today.day)
                    t.mission = m
                    t.save()
                m.save()

        returnDict = {
            "guarder": self.mission_set.filter(time_start__day=today.day,time_start__month=today.month,time_start__year=today.year,template=False),
            "watcher":self.partment.task_set.filter(mission__time_start__day=today.day,mission__time_start__month=today.month,mission__time_start__year=today.year,mission__template=False),
            "driver":self.mission_set.filter(time_start__day=today.day,time_start__month=today.month,time_start__year=today.year,template=False),
            "reliver":self.mission_set.filter(time_start__day=today.day,time_start__month=today.month,time_start__year=today.year,template=False),
            "banker":self.partment.task_set.filter(mission__time_start__day=today.day,mission__time_start__month=today.month,mission__time_start__year=today.year,mission__template=False)
        }
        return returnDict[self.profile]

    class Meta:
        verbose_name = '工作人员'
        verbose_name_plural = '工作人员'



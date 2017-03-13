from django.db import models
from container.models import Container,Car,Gun
from worker.models import Partment,Worker
from . import STATUS
# Create your models here.

import datetime

class Mission(models.Model):
    template = models.BooleanField("是为模板，否为任务",default=True)
    car = models.ForeignKey(Car,verbose_name="执行车")
    worker = models.ManyToManyField(Worker,verbose_name="押运工作人员")
    time_start = models.DateTimeField('开始时间')
    time_end = models.DateTimeField('结束时间')
    guns = models.ManyToManyField(Gun,verbose_name="枪支")
    current_task = models.SmallIntegerField("当前任务",default=0)
    def __str__(self):
        return "{}由{}执行".format(self.time_start,self.car)

    def task_status(self):
        tasks = mission.task_set.order_by('order')
        for t in tasks:
            if t.status != "done":
                return (t.status, t.order)

    def update_current_task(self,order_num):
        if order_num == self.current_task :
            self.current_task = order_num+1
            self.save()

    class Meta:
        verbose_name = '任务'
        verbose_name_plural = '任务'


class Task(models.Model):
    mission_time = models.DateTimeField('节点时间')
    origin = models.ForeignKey(Partment,verbose_name="起始点")
    load_container = models.ManyToManyField(Container,verbose_name="装货箱",blank=True)
    unload_container = models.ManyToManyField(Container,verbose_name="卸货箱",blank=True,related_name="unloading")
    mission = models.ForeignKey(Mission,verbose_name="任务")
    modified = models.DateTimeField('状态改变时间',null=True)
    status = models.CharField('状态',choices=STATUS,max_length=10)
    order = models.SmallIntegerField('顺序', default=0)
    def __str__(self):
        return "在{}执行".format(self.origin)
    def set_status(self,status):
        self.status = status
        self.modified = datetime.datetime.now()
        self.save()
    def load_containers(self):
        if self.status == "failed":
            for c in self.load_container.all():
                c.location = self.mission.car.license
                c.save()
            for c in self.unload_container.all():
                c.location = "从"+self.mission.car.license + "到" +self.origin.name
                c.save()
            self.set_status('load')
            self.mission.update_current_task(self.order)
            self.save()
        if self.status == "receive":
            for c in self.load_container.all():
                c.location = self.mission.car.license
                c.save()
            self.set_status('done')
            self.mission.update_current_task(self.order)
            self.save()


    def receive_containers(self):
        if self.status == "failed":
            for c in self.unload_container.all():
                c.location = self.origin.name
                c.save()
            for c in self.load_container.all():
                c.location = "从"+self.origin.name + "到" +self.mission.car.license
                c.save()
            self.set_status('receive')
            self.save()
        if self.status == "load":
            for c in self.unload_container.all():
                c.location = self.origin.name
                c.save()
            self.set_status('done')
            self.save()

    class Meta:
        verbose_name = '任务节点'
        verbose_name_plural = '任务节点'


# class modifiedTask(models.Model):
#     added = models.DateTimeField('添加时间',auto_now_add=True)
#     banker = models.ForeignKey(Worker,verbose_name='银行验收员')
#     taskTime = models.DateTimeField('任务时间')
#     container = models.ManyToManyField(Container,verbose_name="货箱")
#     def __str__(self):
#         return "{}-{}".format(self.taskTime,self.banker.partment)
#     class Meta:
#         verbose_name = '更改任务节点'
#         verbose_name_plural = '更改任务节点'








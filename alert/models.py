from django.db import models
from task.models import Mission
# Create your models here.
class Alert(models.Model):
    mission = models.ForeignKey(Mission,verbose_name="报警任务")
    added = models.DateTimeField('报警时间',auto_now_add=True)
    status = models.BooleanField('是否解除警报',default=False)
    level = models.CharField("报警等级",choices=(('danger','严重'),('normal','一般')),max_length=20,default="normal")
    memo = models.TextField('备注')
    def __str__(self):
        return "{}于{}报警".format(self.mission.car,self.added)
    class Meta:
        verbose_name = '报警信息'
        verbose_name_plural = '报警信息'

class GunRoutine(models.Model):
    mission = models.ForeignKey(Mission,verbose_name="任务")
    added = models.DateTimeField('取枪或还枪时间',auto_now_add=True)
    content = models.CharField("取枪或还抢",choices=(('return','还枪'),('get','取枪')),max_length=20)
    memo = models.TextField('备注')
    def __str__(self):
        return "{}的枪支记录".format(self.mission)
    class Meta:
        verbose_name = '枪支记录'
        verbose_name_plural = '枪支记录'


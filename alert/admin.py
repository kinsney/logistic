from django.contrib import admin
from .models import Alert,GunRoutine
from django.utils.html import format_html
# Register your models here.
@admin.register(Alert)
class ContainerAdmin(admin.ModelAdmin):
    def detail(self,obj):
        return format_html('<a href="/task/mission/%s/change">点击查看</a>' % obj.mission.pk)
    detail.short_description = '任务详情'
    def doneOrNot(self,obj):
        return bool(obj.status and len(obj.memo))
    doneOrNot.boolean = True
    doneOrNot.short_description = "处理及备案"
    list_display = ('mission','added','detail','doneOrNot','level')

@admin.register(GunRoutine)
class GunRoutineAdmin(admin.ModelAdmin):
    list_display = ('mission','content','added',)

from django.contrib import admin
from .models import Mission,Task
from container.models import Container,Car
from worker.models import Worker
from alert.models import GunRoutine
from django.db.models import Q
# Register your models here.


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('__str__','load_length','unload_length','time_start_str',)
    fields = ('load_container','unload_container')
    def time_start_str(self, obj):
        return obj.mission.time_start.strftime("%H:%M:%S")
    time_start_str.short_description = "任务开始时间"
    def load_length(self,obj):
        return obj.load_container.count()
    load_length.short_description = "出库"
    def unload_length(self,obj):
        return obj.unload_container.count()
    unload_length.short_description = "入库"
    def get_queryset(self,request):
        queryset = super(TaskAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return queryset
        else :
            partment = request.user.worker.partment
            return queryset.filter(origin=partment,mission__template=True)
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            kwargs["queryset"] = Container.objects.all()
        elif db_field.name=='load_container' or db_field.name=='unload_container':
            partment = request.user.worker.partment
            kwargs["queryset"] = Container.objects.filter(partment=partment.parent,status='relaxing')
        return super(TaskAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    filter_horizontal = ('load_container','unload_container')
class TaskInline(admin.TabularInline):
    model = Task
    filter_vertical = ('load_container','unload_container',)
    extra = 0
class GunRoutineInline(admin.TabularInline):
    model = GunRoutine
    extra = 0
@admin.register(Mission)
class MissonAdmin(admin.ModelAdmin):
    def time_start_str(self, obj):
        return obj.time_start.strftime("%Y年%m月%d日 %H:%M:%S")
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name=='car':
            kwargs["queryset"] = Car.objects.filter(status="relaxing")
        return super(MissonAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    def completed_car(self,obj):
        tasks = obj.task_set.all()
        dones = obj.task_set.filter(Q(status='done')|Q(status='load'))
        if tasks.count()>0:
            return str(round(dones.count()/tasks.count()*100)) + "%"
        else :
            return "未知"
    def completed_bank(self,obj):
        tasks = obj.task_set.all()
        confirms = obj.task_set.filter(Q(status='done')|Q(status='receive'))
        if tasks.count()>0:
            return str(round(confirms.count()/tasks.count()*100)) + '%'
        else :
            return "未知"
    completed_car.short_description = "押运任务进度"
    completed_bank.short_description = "网点确认进度"
    time_start_str.admin_order_field = 'time_start'
    time_start_str.short_description = "任务开始时间"
    def time_end_str(self, obj):
        return obj.time_end.strftime("%Y年%m月%d日 %H:%M:%S")
    time_end_str.admin_order_field = 'time_end'
    time_end_str.short_description = "任务结束时间"
    search_fields = ['car']
    inlines = (TaskInline,GunRoutineInline)
    list_display = ('__str__','time_start_str','car','completed_car','completed_bank','template')
    list_filter = ('time_start','car','template')
    filter_vertical = ('worker','guns')
    def change_view(self,request,object_id,form_url="",extra_context=None):
        mission = Mission.objects.get(pk=object_id)
        return super(MissonAdmin, self).change_view(
            request, object_id, form_url, extra_context={"mission":mission},
        )
    change_form_template = "admin/task/change.html"



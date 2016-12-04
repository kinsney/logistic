from django.contrib import admin
from .models import Mission,Task
# Register your models here.


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass
class TaskInline(admin.TabularInline):
    model = Task
    filter_horizontal = ('load_container','unload_container',)
    extra = 0

@admin.register(Mission)
class MissonAdmin(admin.ModelAdmin):
    def time_start_str(self, obj):
        return obj.time_start.strftime("%Y年%m月%d日 %H:%M:%S")
    time_start_str.admin_order_field = 'time_start'
    time_start_str.short_description = "任务开始时间"
    def time_end_str(self, obj):
        return obj.time_end.strftime("%Y年%m月%d日 %H:%M:%S")
    time_end_str.admin_order_field = 'time_end'
    time_end_str.short_description = "任务结束时间"
    search_fields = ['car']
    inlines = (TaskInline,)
    list_display = ('__str__','time_start_str','time_end_str')
    filter_horizontal = ('worker',)


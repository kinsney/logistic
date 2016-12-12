from django.contrib import admin
from .models import Partment,Worker
from django.utils.html import format_html
# Register your models here.


@admin.register(Partment)
class PartmentAdmin(admin.ModelAdmin):
    search_fields = ['name','parent']
    list_display = ('name','parent','location')
    list_filter = ('parent',)


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    search_fields = ['name','workerId']
    list_display = ('name','user','profile','partment','inline_image')
    list_filter = ('profile','partment')
    def inline_image(self,obj):
        return format_html('<img src="%s" style="height:64px"/>' % obj.avatar.url)
    inline_image.short_description = "头像"




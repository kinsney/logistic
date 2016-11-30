from django.contrib import admin
from .models import Partment,Worker
# Register your models here.


@admin.register(Partment)
class PartmentAdmin(admin.ModelAdmin):
    search_fields = ['name','parent']
    list_display = ('name','parent','location')

@admin.register(Worker)
class DriverAdmin(admin.ModelAdmin):
    search_fields = ['name','workerId']
    list_display = ('user','name','partment')

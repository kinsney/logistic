from django.contrib import admin
from .models import Container,Car
# Register your models here.
@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    search_fields = ['number','partment','location']
    list_display = ('number','partment','location','status')

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    search_fields = ['license']
    list_display = ('license','status')

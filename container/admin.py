from django.contrib import admin
from .models import Container,Car,Gun,GunType
from worker.models import Partment
# Register your models here.
@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    search_fields = ['number','partment','location']
    list_display = ('number','partment','location','status')
    list_filter = ('partment','location','status')
    def get_queryset(self,request):
        queryset = super(ContainerAdmin, self).get_queryset(request)
        securePartment = Partment.objects.get(pk=1)
        if request.user.is_superuser or request.user.worker.partment == securePartment:
            return queryset
        else :
            partment = request.user.worker.partment.parent
            return queryset.filter(partment=partment)

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    search_fields = ['license']
    list_display = ('license','status')

@admin.register(Gun)
class GunAdmin(admin.ModelAdmin):
    list_display = ('number','type','status')
    list_filter = ('type','status')

@admin.register(GunType)
class GunTypeAdmin(admin.ModelAdmin):
    pass

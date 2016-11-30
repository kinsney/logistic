from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^mission$',views.get_mission,name='get_mission'),
]

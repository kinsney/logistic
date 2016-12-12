from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^get_mission_driver$',views.get_mission_driver,name='get_mission_driver'),
    url(r'^get_mission_watcher$',views.get_mission_watcher,name='get_mission_watcher'),
    url(r'^update_task_driver$',views.update_task_driver,name='update_task_driver'),
    url(r'^update_task_watcher$',views.update_task_watcher,name='update_task_watcher'),
]

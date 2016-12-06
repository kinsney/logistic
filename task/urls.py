from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^get_mission_driver$',views.get_mission_driver,name='get_mission_driver'),
    url(r'^get_mission_watcher$',views.get_mission_watcher,name='get_mission_watcher'),
    url(r'^update_task_driver_load$',views.update_task_driver_load,name='update_task_driver_load'),
    url(r'^update_task_driver_unload$',views.update_task_driver_unload,name='update_task_driver_unload'),
    url(r'^update_task_watcher_push$',views.update_task_watcher_push,name='update_task_watcher_push'),
    url(r'^update_task_watcher_receive$',views.update_task_watcher_receive,name='update_task_watcher_receive'),
]

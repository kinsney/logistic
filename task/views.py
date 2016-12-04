from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, Http404, HttpResponseNotFound
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import logging
logger = logging.getLogger("django")
@csrf_exempt
def get_mission(request):
    user = User.objects.get(username=request.POST["phone"])
    missions = user.worker.get_today_mission()
    missionInfos = []
    #print(missions)
    for mission in missions:
        guarders = mission.worker.filter(profile="guarder")
        driver = mission.worker.get(profile="driver")
        tasks = mission.task_set.order_by('order')
        car = mission.car
        guardersInfo = []
        for guarder in guarders:
            guarderInfo = {
                "name":guarder.name,
                "workerId":guarder.workerId,
                "avatar":settings.SITE_URL + guarder.avatar.url,
                "phone":guarder.user.username
            }
            guardersInfo.append(guarderInfo)
        tasksInfo = []
        for task in tasks:
            load_containers = task.load_container.all()
            load_containersInfo = []
            for load_container in load_containers:
                load_containerInfo = {
                    "number":load_container.number,
                }
                load_containersInfo.append(load_containerInfo)
            unload_containers = task.unload_container.all()
            unload_containersInfo = []
            for unload_container in unload_containers:
                unload_containerInfo = {
                    "number":unload_container.number,
                }
                unload_containersInfo.append(unload_containerInfo)
            taskInfo = {
                "origin":task.origin.name,
                "target":task.target.name,
                #"parent":task.target.parent.name,
                "status":task.status,
                "load_containers":load_containersInfo,
                "unload_containers":unload_containersInfo
            }
            tasksInfo.append(taskInfo)
        missionInfo = {
            "car":{
                "license":car.license,
                "status":car.status
            },
            "driver":{
                "name":driver.name,
                "workerId":driver.workerId,
                "avatar":settings.SITE_URL + driver.avatar.url,
                "phone":driver.user.username
            },
            "guarders":guardersInfo,
            "time_start":mission.time_start.strftime("%Y-%m-%d %H:%M:%S"),
            "time_end":mission.time_end.strftime("%Y-%m-%d %H:%M:%S"),
            "tasksInfo":tasksInfo
        }
        missionInfos.append(missionInfo)
    return HttpResponse(json.dumps(missionInfos))





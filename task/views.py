from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, Http404, HttpResponseNotFound
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from task.models import Task
import json
import logging
logger = logging.getLogger("django")
@csrf_exempt
def get_mission_driver(request):
    #user = User.objects.get(username=request.POST["phone"])
    user = User.objects.get(username="bamf")
    missions = user.worker.get_today_mission()
    missionInfos = []
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
                "task_pk":task.pk,
                "origin":task.origin.name,
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
            "tasksInfo":tasksInfo,
            "current_task":mission.current_task,
            "mission_pk":mission.pk
        }
        missionInfos.append(missionInfo)
    return HttpResponse(json.dumps(missionInfos))

@csrf_exempt
def get_mission_watcher(request):
    #user = User.objects.get(username=request.POST["phone"])
    user = User.objects.get(username="supervisor")
    tasks = user.worker.get_today_mission()
    taskInfos = []
    for t in tasks:
        guarders = t.mission.worker.filter(profile="guarder")
        driver = t.mission.worker.get(profile="driver")
        car = t.mission.car
        guardersInfo = []
        for guarder in guarders:
            guarderInfo = {
                "name":guarder.name,
                "workerId":guarder.workerId,
                "avatar":settings.SITE_URL + guarder.avatar.url,
                "phone":guarder.user.username
            }
            guardersInfo.append(guarderInfo)

        load_containers = t.load_container.all()
        load_containersInfo = []
        for load_container in load_containers:
            load_containerInfo = {
                "number":load_container.number,
            }
            load_containersInfo.append(load_containerInfo)

        unload_containers = t.unload_container.all()
        unload_containersInfo = []
        for unload_container in unload_containers:
            unload_containerInfo = {
                "number":unload_container.number,
            }
            unload_containersInfo.append(unload_containerInfo)
        taskInfo = {
                "task_pk":t.pk,
                "origin":t.origin.name,
                "status":t.status,
                "load_containers":load_containersInfo,
                "unload_containers":unload_containersInfo
            }
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
            "taskInfo":taskInfo
        }
        taskInfos.append(missionInfo)
    return HttpResponse(json.dumps(taskInfos))


@csrf_exempt
def update_task_watcher(request):
    task = Task.objects.get(pk=57)
    task.receive_containers()

@csrf_exempt
def update_task_driver(request):
    task = Task.objects.get(pk=57)
    task.load_containers()
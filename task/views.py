from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, Http404, HttpResponseNotFound
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from task.models import Task,Mission
from alert.models import Alert,GunRoutine
from container.models import Car
from worker.models import Worker
import json
import datetime

def getMission(mission):
    containers = []
    guarders = mission.worker.filter(profile="guarder")
    driver = mission.worker.get(profile="driver")
    relivers = mission.worker.filter(profile="reliver")
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
    reliversInfo = []
    for reliver in relivers:
        reliverInfo = {
            "name":reliver.name,
            "workerId":reliver.workerId,
            "avatar":settings.SITE_URL + reliver.avatar.url,
            "phone":reliver.user.username
        }
        reliversInfo.append(reliverInfo)
    tasksInfo = []
    for task in tasks:
        load_containers = task.load_container.all()
        load_containersInfo = []
        for load_container in load_containers:
            load_containersInfo.append(load_container.number)
        if task.status == "done" or task.status == "load":
            containers = containers + load_containersInfo
        unload_containers = task.unload_container.all()
        unload_containersInfo = []
        for unload_container in unload_containers:
            unload_containersInfo.append(unload_container.number)
        if task.status == "done" or task.status == "load":
            containers = list(set(containers).difference(set(unload_containersInfo)))
        taskInfo = {
            "task_pk":task.pk,
            "origin":task.origin.__str__(),
            "status":task.status,
            "load_containers":load_containersInfo,
            "unload_containers":unload_containersInfo
        }
        tasksInfo.append(taskInfo)
    alert = mission.alert_set.filter(status=False)
    gunsInfo = []
    for gun in mission.guns.all():
        gunsInfo.append(gun.number)
    returnGun = 0
    getGun = 0
    for routine in mission.gunroutine_set.all():
        if routine.content == 'return':
            returnGun = 1
        if routine.content == 'get':
            getGun = 1
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
        "relivers":reliversInfo,
        "time_start":mission.time_start.strftime("%Y-%m-%d %H:%M:%S"),
        "time_end":mission.time_end.strftime("%Y-%m-%d %H:%M:%S"),
        "tasksInfo":tasksInfo,
        "current_task":mission.current_task,
        "mission_pk":mission.pk,
        "alert":len(alert),
        "containers":containers,
        "guns":gunsInfo,
        "getGun":getGun,
        "returnGun":returnGun
    }
    return missionInfo
@csrf_exempt
def get_mission_driver(request):
    try:
        user = User.objects.get(username=request.POST["phone"])
    except:
        return HttpResponseForbidden()
    try:
        missions = user.worker.get_today_mission().order_by('time_start')
        missionInfos = []
        for mission in missions:
            missionInfo = getMission(mission)
            missionInfos.append(missionInfo)
    except:
        return HttpResponseBadRequest()
    return HttpResponse(json.dumps(missionInfos))

@csrf_exempt
def print_get_mission_driver(request):
    try:
        worker = Worker.objects.get(pk=request.POST["pk"])
    except:
        return HttpResponseForbidden()
    try:
        missions = worker.get_today_mission().order_by('time_start')
        missionInfos = []
        for mission in missions:
            missionInfo = getMission(mission)
            missionInfos.append(missionInfo)
    except:
        return HttpResponseBadRequest()
    return HttpResponse(json.dumps(missionInfos))

@csrf_exempt
def get_mission_watcher(request):
    user = User.objects.get(username=request.POST["phone"])
    tasks = user.worker.get_today_mission().order_by('mission_time')
    taskInfos = []
    for t in tasks:
        guarders = t.mission.worker.filter(profile="guarder")
        relivers = t.mission.worker.filter(profile="reliver")
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
        reliversInfo = []
        for reliver in relivers:
            reliverInfo = {
                "name":reliver.name,
                "workerId":reliver.workerId,
                "avatar":settings.SITE_URL + reliver.avatar.url,
                "phone":reliver.user.username
            }
            reliversInfo.append(reliverInfo)
        load_containers = t.load_container.all()
        load_containersInfo = []
        for load_container in load_containers:
            load_containersInfo.append(load_container.number)

        unload_containers = t.unload_container.all()
        unload_containersInfo = []
        for unload_container in unload_containers:
            unload_containersInfo.append(unload_container.number)
        taskInfo = {
                "task_pk":t.pk,
                "origin":t.origin.name,
                "status":t.status,
                "order":t.order,
                "start_time":t.mission_time.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time":t.mission.time_end.strftime("%Y-%m-%d %H:%M:%S"),
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
            "relivers":reliversInfo,
            "taskInfo":taskInfo
        }
        taskInfos.append(missionInfo)
    return HttpResponse(json.dumps(taskInfos))
@csrf_exempt
def get_gunjobs(request):
    today = datetime.date.today()
    missions = Mission.objects.filter(time_start__day=today.day,time_start__month=today.month,time_start__year=today.year,template=False)
    cars = Car.objects.filter(status="relaxing",mission__in=missions).distinct()
    gunjobs = []
    for car in cars:
        missions = missions.filter(car=car)
        infos = []
        for mission in missions:
            missionInfo = getMission(mission)
            infos.append(missionInfo)
        gunjob = {
            "car":car.license,
            "info":infos
        }
        gunjobs.append(gunjob)
    return HttpResponse(json.dumps(gunjobs))
@csrf_exempt
def update_task_watcher(request):
    user = User.objects.get(username=request.POST["phone"])
    pk = request.POST['task_pk']
    task = Task.objects.get(pk=pk)
    task.receive_containers()
    status = {"status":task.status}
    return HttpResponse(json.dumps(status))

@csrf_exempt
def update_task_driver(request):
    try:
        user = User.objects.get(username=request.POST["phone"])
        pk = request.POST['task_pk']
        task = Task.objects.get(pk=pk)
        task.load_containers()
        mission = task.mission
        missionInfo = getMission(mission)
        return HttpResponse(json.dumps(missionInfo))
    except:
        return HttpResponseForbidden()

@csrf_exempt
def update_routine(request):
    try:
        pk = request.POST['id']
        content = request.POST['content']
        mission = Mission.objects.get(pk=pk)
        routine = GunRoutine.objects.create(mission=mission,content=content)
        missionInfo = getMission(mission)
        return HttpResponse(json.dumps(missionInfo))
    except:
        return HttpResponseForbidden()


@csrf_exempt
def handset_report(request):
    task_pk = request.POST['task_pk']
    task = Task.objects.get(pk=task_pk)
    if task.status == 'load' or task.status == 'receive':
        task.status = 'done'
        task.save()
    mission = task.mission
    missionInfo = getMission(mission)
    return HttpResponse(json.dumps(missionInfo))

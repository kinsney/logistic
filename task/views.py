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
    for mission in missions:
        guarders = mission.worker.filter(profile="guarder")
        driver = mission.worker.get(profile="driver")
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
            "time_end":mission.time_end.strftime("%Y-%m-%d %H:%M:%S")

        }
        missionInfos.append(missionInfo)
    return HttpResponse(json.dumps(missionInfos))


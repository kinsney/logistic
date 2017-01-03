from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, Http404, HttpResponseNotFound
from django.contrib.auth import authenticate,login as do_login, logout as do_logout
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.middleware import csrf
from django.forms.models import model_to_dict
from django.conf import settings
from container.models import Container
import os
import logging
import json
# Create your views here.
def login_required(view):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view(request, *args, **kwargs)
        elif request.is_ajax():
            return HttpResponseForbidden()
    return wrapped_view
@csrf_exempt
def csrf_login(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        assert len(username) > 0
    except (KeyError,AssertionError):
        return HttpResponseBadRequest()
    user = authenticate(username=username,password=password)
    if user is None:
        return HttpResponseForbidden()
    do_login(request,user)
    partment_containers = Container.objects.filter(partment=user.worker.partment,status='relaxing')
    extra = {
        "phone":user.username,
        "partment":user.worker.partment.__str__(),
        "profile":user.worker.profile,
        "name":user.worker.name,
        "personId":user.worker.personId,
        "avatar":settings.SITE_URL + user.worker.avatar.url
    }
    userInfo = model_to_dict(user.worker)
    userInfo.update(extra)
    return HttpResponse(json.dumps(userInfo))




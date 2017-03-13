from django.http import HttpResponse
from channels.handler import AsgiHandler
from task.models import Mission
from .models import Alert
from channels import Group
from django.shortcuts import render,get_object_or_404
def ws_add(message):
    message.reply_channel.send({"accept": True})
    Group("alert").add(message.reply_channel)

def ws_message(message):
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
    try:
        action = message.content['text'].split('-')[0]
        if action == "lock":
            mission_id = message.content['text'].split('-')[1]
            level = message.content['text'].split('-')[2]
            mission = get_object_or_404(Mission,pk=mission_id)
            alert = Alert.objects.create(mission=mission,level=level)
        elif action == "unlock":
            alert_id = message.content['text'].split('-')[2]
            alert = get_object_or_404(Alert,pk=alert_id)
            alert.status=True
            alert.save()
        Group('alert').send({
            "text":"%s" % message.content['text']
        })
    except:
        pass

def ws_disconnect(message):
    Group("alert").discard(message.reply_channel)



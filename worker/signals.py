from django.db.models import signals
from django.dispatch import receiver
import os
from .models import Worker,PrintVerision
from logistic.settings import MEDIA_ROOT
from .zip import zip_dir
@receiver(signals.post_init, sender=Worker)
def change_version(instance, **kwargs):
    instance.original_fingerPrint = instance.fingerPrint

@receiver(signals.post_save, sender=Worker)
def change_version(instance,created,**kwargs):
    if  instance.original_fingerPrint != instance.fingerPrint:
            print_url = os.path.join(MEDIA_ROOT,'prints')
            output = os.path.join(MEDIA_ROOT,'prints.zip')
            zip_dir(print_url,output)
            version = PrintVerision.objects.all()[0]
            version.number = version.number + 1
            version.save()


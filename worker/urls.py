from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^csrf_login$',views.csrf_login,name='login'),
]

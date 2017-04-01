from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^csrf_login$',views.csrf_login,name='login'),
    url(r'^print_login$',views.print_login,name='print_login'),
    url(r'^version$',views.version,name='version'),
]

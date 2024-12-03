from django.urls import path

from . import views

urlpatterns=[
    path("/",views.mqttIndex),
    #path("/upload",views.upload,name="upload"),
]
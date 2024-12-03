from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
# Create your views here.
def mqttIndex(request):
    template=loader.get_template("mqttclient/mqttclient.html")
    context={}
    return HttpResponse(template.render(context=context,request=request))
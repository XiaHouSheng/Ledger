from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests
import gzip
from io import BytesIO
import json
import time
import base64
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    template=loader.get_template("Ledger/index.html")
    timetable=["游戏","游戏","游戏"]
    timestamp=time.strftime("今天是%Y-%m-%d %a", time.localtime())
    context={"timetable":timetable,"weather":weather("岐山"),"timestamp":timestamp,"classes":todayclass()}
    return HttpResponse(template.render(context=context,request=request))

def weather(city="兰州"):
    geourl="https://geoapi.qweather.com/v2/city/lookup"
    parageo={
        "key":"730c19727ff745b1bfcf5410b74673ef",
        "location":city,
    }
    locationID=json.loads(requests.get(geourl,params=parageo).text)["location"][0]["id"]
    weatherurl="https://devapi.qweather.com/v7/weather/3d"
    paraweather={
        "key":"730c19727ff745b1bfcf5410b74673ef",
        "location":locationID,
    }
    response_json=json.loads(requests.get(weatherurl,params=paraweather).text)
    daily=[{"date":i["fxDate"],"tday":i["textDay"],"icon_path":"images/icons/"+i["iconDay"]+".svg"} for i in response_json["daily"]]
    update_time=response_json["updateTime"].split("+")[0].replace("T"," ")
    today={"tday":response_json["daily"][0]["textDay"],"icon_path":"images/icons/"+response_json["daily"][0]["iconDay"]+".svg","temp":response_json["daily"][0]["tempMax"]+"°"}
    return {"update_time":update_time,"daily":daily,"today":today,"city":city}
    
def todayclass():
    classes={
        "Mon":["高等数学|8:00-9:50|4-17周","大学英语|10:10-12:00|5-19周(单)","C/C++程序设计|14:30-16:20|4-11周"],
        "Tue":["体育|10:10-12:00|4-19周"],
        "Wed":["C/C++程序设计|8:00-9:50|4-11周","高等数学|10:10-12:00|4-12周","军事理论|14:30-16:20|12-17周"],
        "Thu":["形势与政策|8:00-9:50|11-12周","思想道德|10:10-12:00|4-19周","物联网工程|14:30-16:20|4-11周","大学英语|16:40-18:30|4-18周(双)"],
        "Fri":["高等数学|10:10-12:00|4-17周"],
        "Sat":["老弟你没课啊"],
        "Sun":["老弟你没课啊"]
    }
    return classes[time.strftime("%a")]




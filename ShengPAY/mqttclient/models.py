from django.db import models

# Create your models here.
#服务器ip 
#对应的topic
#对应topic的msg
#时间 msg内容 类型

#表1 存储服务器ip对
#表2 topic对应的msg

#server->对应多个topic->topic对应多个msg

class MqttServer(models.Model):
    #服务器地址
    server = models.CharField(max_length=16)


class MqttTopic(models.Model):

    server = models.ForeignKey(MqttServer,on_delete=models.CASCADE,related_name="topic")

    topic = models.CharField(max_length=30)

class MqttMessage(models.Model):
    #topic
    topic = models.ForeignKey(MqttTopic,on_delete=models.CASCADE,related_name="message")
    #msg
    message = models.JSONField()
    #msg时间
    rastime = models.DateTimeField(auto_now_add=True)
    #type client发送的还是接受的 0发送 1接收
    msgtype = models.IntegerField()

#注册到admin中
from django.contrib import admin
from .models import MqttServer,MqttTopic,MqttMessage
admin.site.register(MqttServer)
admin.site.register(MqttTopic)
admin.site.register(MqttMessage)


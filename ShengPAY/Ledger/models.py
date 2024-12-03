from django.db import models


class Status(models.IntegerChoices):
    #运动
    SPORT=1,"运动"
    #吃饭
    MEALS=2,"吃饭"
    #游戏
    GAMES=3,"娱乐"
    #学习
    STUDY=4,"学习"
    #借钱
    LEADING=5,"借钱"

class Ledger(models.Model):
    # 备注 char
    details=models.CharField(max_length=200)
    # 金钱 float
    nummoney=models.FloatField()
    # 时间 自带
    paytime=models.DateField(auto_now_add=True)
    # 类型 int
    paytype=models.IntegerField(choices=Status.choices,default=Status.STUDY)
    
#注册
from django.contrib import admin
from .models import Ledger
admin.site.register(Ledger)

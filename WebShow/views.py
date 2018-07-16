#coding=utf8
from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse,StreamingHttpResponse
from WebShow.models import User,PM25
import json
from urllib.parse import quote
from os import path
import datetime
from os import mkdir
import random

def login(request):
    return render(request, 'login.html')

def userlogin(request):
    if request.session.get('username') is not None:
        return HttpResponseRedirect('/map')
    if request.method == "GET":
        username = request.GET['username']
        password = request.GET['password']
        usercount = User.objects.filter(username__exact=username, password__exact = password).count()
        if usercount>=1:
            request.session['username'] = username
            request.session.set_expiry(1800)
            print("login")
            if User.objects.get(username__exact=username, password__exact=password).authority >= 1:
                print("login")
                request.session['authority'] = 1
                return HttpResponseRedirect('/map')
            else:
                print("login")
                request.session['authority'] = 0
                return HttpResponseRedirect('/map')
        else:
            print("login fail")
    return HttpResponseRedirect('/login/')

def logout(request):
    del request.session["username"]
    print("exit")
    return HttpResponseRedirect('/login/')

def map(request):
    count = PM25.objects.filter().count()
    if count>10:
        list = PM25.objects.filter().order_by("id")[count-10:count]
    else:
        list = PM25.objects.filter().order_by("id")[0:10]
    result = {}
    for item in list:
        result[item.id] = {'id':item.id,'longtitude':item.longtitude,'latitude':item.latitude,'time':str(item.time),"value":item.value}
    print(result)
    result = sorted(result.items(),key=lambda x:x[0])
    print(result)
    return render(request, 'map.html',{'result':result})

def getrecord(request):
    maxid = request.GET['maxid']
    count = PM25.objects.filter(id__gt=maxid).count()
    if count > 10:
        list = PM25.objects.filter().order_by("id")[count - 10:count]
    else:
        list = PM25.objects.filter(id__gt=maxid).order_by("id")[0:10]
    result = []
    for item in list:
        result.append({"id":str(item.id),"longtitude":str(item.longtitude),"latitude":str(item.latitude),"time":str(item.time),"value":str(item.value)})
    print(result)
    return HttpResponse(json.dumps(result), content_type="application/json")


def getresult(request):
    print("getresult")
    latitude = request.POST['latitude']
    longtitude = request.POST['longtitude']
    aim = request.POST["aim"]
    print('('+str(latitude)+','+str(longtitude)+")"+" "+aim)
    value = random.randint(0,5000)
    print("random",value)
    return HttpResponse(aim+"+"+str(value),content_type="text/html")

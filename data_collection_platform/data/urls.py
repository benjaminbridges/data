"""data_collection_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('orglist', orglist, name='orglist'),
    path('orgdetail/<int:id>', orgdetail, name='orgdetail'),
    path('orgnew', orgnew, name='orgnew'),
    path('orgedit/<int:oid>', orgedit, name='orgedit'),

    path('entitylist', entitylist, name='entitylist'),
    path('entitydetail/<int:id>', entitydetail, name='entitydetail'),
    path('entitynew', entitynew, name='entitynew'),
    path('entityedit/<int:eid>', entityedit, name='entityedit'),

    path('userlist', userlist, name='userlist'),
    path('userdetail/<int:id>', userdetail, name='userdetail'),
    path('usernew', usernew, name='usernew'),
    path('useredit/<int:id>', useredit, name='useredit'),

    path('surveylist', surveylist, name='surveylist'),
    path('surveyaddentity/<int:sid>', surveyaddentity, name='surveyaddentity'),

    path('surveydetail/<int:sid>', surveydetail, name='surveydetail'),
    path('surveydelete/<int:sid>', surveydelete, name='surveydelete'),
    path('surveyclose/<int:sid>', surveyclose, name='surveyclose'),
    path('surveynew', surveynew, name='surveynew'),
    path('surveyedit/<int:id>', surveyedit, name='surveyedit'),

    path('surveycentaltimes/<int:id>', surveycentaltimes, name='surveycentaltimes'),
    path('surveycentaltimesedit/<int:id>', surveycentaltimesedit, name='surveycentaltimesedit'),

    path('questionnew/<int:id>', questionnew, name='questionnew'),
    path('questionedit/<int:sid>/<int:qid>', questionedit, name='questionedit'),
    path('questionadd/<int:id>', questionadd, name='questionadd'),
    path('questiondelete/<int:sid>/<int:qid>', questiondelete, name='questiondelete'),

    path('breakdowncategorynew/<int:id>', breakdowncategorynew, name='breakdowncategorynew'),
    path('breakdowncategoryedit/<int:sid>/<int:bcid>', breakdowncategoryedit, name='breakdowncategoryedit'),
    path('breakdowncategoryadd/<int:id>', breakdowncategoryadd, name='breakdowncategoryadd'),
    path('breakdowncategorydelete/<int:sid>/<int:bcid>', breakdowncategorydelete, name='breakdowncategorydelete'),

    path('surveybreakdown/<int:sid>/<int:eid>/<int:seid>', surveybreakdown, name='surveybreakdown'),
    path('surveybreakdownedit/<int:sid>/<int:eid>/<int:seid>', surveybreakdownedit, name='surveybreakdownedit'),

    path('surveyfinalcheck/<int:sid>/<int:eid>/<int:seid>', surveyfinalcheck, name='surveyfinalcheck'),

    path('surveyadmin', surveyadmin, name='surveyadmin'),
    path('mysurveys', mysurveys, name='mysurveys'),
    path('allsurveys', allsurveys, name='allsurveys'),
    path('surveyinstance/<int:sid>/<int:eid>/<int:seid>', surveyinstance, name='surveyinstance'),
    path('answers/<int:siid>/<int:qid>', answers, name='answers'),
    path('surveyinstancerejection/<int:siid>', surveyinstancerejection, name='surveyinstancerejection'),
    path('surveyinstanceallrejection/<int:siid>', surveyinstanceallrejection, name='surveyinstanceallrejection'),

    path('surveybreakdowndelete/<int:bdid>/<int:sid>/<int:eid>/<int:seid>/', surveybreakdowndelete, name='surveybreakdowndelete'),
    path('surveybreakdownadd/<int:sid>/<int:eid>/<int:seid>', surveybreakdownadd, name='surveybreakdownadd'),
    path('surveybreakdownuseradd/<int:bdid>/<int:sid>/<int:eid>/<int:seid>/', surveybreakdownuseradd, name='surveybreakdownuseradd'),
    path('surveybreakdownuserdelete/<int:pid>/<int:bdid>/<int:sid>/<int:eid>/<int:seid>/', surveybreakdownuserdelete, name='surveybreakdownuserdelete'),

]

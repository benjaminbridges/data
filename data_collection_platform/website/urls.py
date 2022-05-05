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
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from .views import info, contact, loginpage, logoutUser, myprofile




#from data.views import orglist, orgdetail, entitylist, entitydetail


urlpatterns = [
    path('info', info, name='info'),
    path('contact', contact, name='contact'),
    path('loginpage', loginpage, name='loginpage'),
    path('logoutUser', logoutUser, name='logoutUser'),
    #path('registerpage', registerpage, name='registerpage'),
    path('myprofile', myprofile, name='myprofile'),

    path("reset_password/", auth_views.PasswordResetView.as_view(template_name="website/passwordreset.html"), name="reset_password"),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(template_name="website/passwordresetdone.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="website/passwordresetform.html"), name="password_reset_confirm"),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(template_name="website/passwordresetsent.html"), name="password_reset_complete")

]

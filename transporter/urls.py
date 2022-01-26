from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('',views.logins,name='logins'),
    path('registers/',views.registers,name='registers'),
    path('otps/',views.otps,name='otps'),
    path('homes/',views.homes,name='homes'),
    path('logouts/',views.logouts,name='logouts'),
    path('forgot-passwords/',views.forgot_passwords,name='forgot-passwords'),
    path('profiles/',views.profiles,name='profiles'),
    path('view-orders/',views.view_orders,name='view-orders'),
    path('complete-dels/<int:pk>', views.complete_dels,name='complete-dels'),
]
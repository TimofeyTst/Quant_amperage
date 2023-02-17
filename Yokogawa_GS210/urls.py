from django.urls import path

from Yokogawa_GS210.views import *

urlpatterns = [
    path('', index, name="Yokogawa_GS210"),
    path('update_a/', update_a, name="Yokogawa_GS210_update_a"),
    path('update_v/', update_v, name="Yokogawa_GS210_update_v"),
    path('connect/', connect, name="Yokogawa_GS210_connect"),
]

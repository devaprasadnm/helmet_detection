from django.urls import path
from . import views

urlpatterns = [
    path('',views.img,name="img"),
    path('img_feed',views.img_feed,name="img_feed"),
]

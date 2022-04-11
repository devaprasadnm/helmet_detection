from django.urls import path
from . import views

urlpatterns = [
    path('',views.video,name="video"),
    path('video_feed',views.video_feed,name="video_feed"),
]

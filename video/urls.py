
from django.urls import path, include
from . import views

urlpatterns = [
    path('videos/', views.YoutubeData.as_view(),name = "To fetch videos")
]

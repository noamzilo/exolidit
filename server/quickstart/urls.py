from django.urls import path

from server.quickstart import views

urlpatterns = [
    path('', views.index, name='index'),
]
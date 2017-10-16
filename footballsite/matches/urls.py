from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^competitions$', views.find_competitions, name='find_competitions'),
    url(r'^$', views.index, name='index'),
]

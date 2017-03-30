#from django.contrib import admin
from django.conf.urls import url
#from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$',views.log),
    url(r'^logout$', views.logout),
    url(r'^wish/(?P<id>\d+)$', views.wish, name='wish'),
    url(r'^wish/create$', views.add_new, name='add_new'),
    url(r'^create_item$', views.create_item, name='create_item'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^add/(?P<id>\d+)$', views.add, name='add'),
    url(r'^delete_item/(?P<id>\d+)$', views.delete, name='delete'),
    url(r'^remove_item/(?P<id>\d+)$', views.remove, name='remove'),

]

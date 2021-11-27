from django.urls import path, include
from rest_framework import routers, urlpatterns
from rest_framework.routers import DefaultRouter
from cleaning_rec import views

router = routers.DefaultRouter()
router.register('cleaning_rec', views.UberDriverViewSets)

app_name = 'cleaning_rec'

urlpatterns = [
    path('', include(router.urls)),
]

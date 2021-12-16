from django.urls import path, include
from rest_framework import routers, urlpatterns
from rest_framework.routers import DefaultRouter
from cleaning_rec import views
from .views import CreateCleaningRecordsViewSets, GenerateRecords

router = routers.DefaultRouter()
router.register('driver', views.UberDriverViewSets, basename='driver')
router.register('create-records', views.CreateCleaningRecordsViewSets, basename='create-records')

app_name = 'cleaning_rec'

urlpatterns = [
    path('', include(router.urls)),
    path('folder/<str:folder_name>/', views.GenerateRecords.as_view(), name='folder'),
]

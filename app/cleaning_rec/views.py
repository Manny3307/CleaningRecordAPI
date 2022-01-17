from django.views.generic.base import View
from rest_framework import request, viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from core.models import CreateCleaningRecords, UberDriver, UberDriverCPVVCertificate, UberTempCleaningRecords
from cleaning_rec import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from cleaning_rec.Callable.UberCleaningRecordBuilder import UberCleaningRecordBuilder
from django.db import transaction
from cleaning_rec.Helpers import ExceptionLogging
import json

class UberDriverViewSets(viewsets.ModelViewSet):
    '''Manage Driver Details in the Database'''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = UberDriver.objects.all()
    serializer_class = serializers.UberDriverSerializer

    def get_queryset(self):
        '''Return objects for the current authenticated user only'''
        
        queryset = self.queryset
        return queryset

    def perform_create(self, serializer):
        '''Create a new record for a Ride Share Driver'''
        serializer.save()


class CreateCleaningRecordsViewSets(viewsets.ModelViewSet):
    '''Manage Driver Details in the Database'''
    #ExceptionLogging.UberExceptionLogging.UberLogException()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = CreateCleaningRecords.objects.all()
    serializer_class = serializers.CreateRecordsSerializer

    def get_queryset(self):
        foldername = self.request.query_params.get('folder_name', None)
        #print(foldername)


    def perform_create(self, Datafile):
        '''Create cleaning records and save the folder name to database for a Ride Share Driver'''
        DriverInput = Datafile
        folder_name = DriverInput["folder_name"]
        csv_file_name = DriverInput["csv_file_name"]
        objUberClean = UberCleaningRecordBuilder()
        objUberClean.execRecordBuilderFunctionality(folder_name.value, csv_file_name.value)

class GenerateRecords(APIView):
    '''Genreate the cleaning records for the logged in driver'''
    def get(self, request, *args, **kwargs):
        if kwargs.get("folder_name", None) is not None:
            csv_driver_record_file = kwargs["csv_file_name"]
            FolderName = kwargs["folder_name"]
            print(f"Get = {FolderName}, {csv_driver_record_file}")
            #objUberClean = UberCleaningRecordBuilder()
            #objUberClean.execRecordBuilderFunctionality(FolderName, csv_driver_record_file)
        return Response()

    def post(self, request, *args, **kwargs):
        if kwargs.get("folder_name", None) is not None:
            csv_driver_record_file = kwargs["csv_file_name"]
            FolderName = kwargs["folder_name"]
            print(f"Post = {FolderName}, {csv_driver_record_file}")
            #objUberClean = UberCleaningRecordBuilder()
            #objUberClean.execRecordBuilderFunctionality(FolderName, csv_driver_record_file)
        return Response()
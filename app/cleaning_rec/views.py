from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from core.models import CreateCleaningRecords, UberDriver
from cleaning_rec import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from cleaning_rec.Callable import UberCleaningRecordBuilder

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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = CreateCleaningRecords.objects.all()
    serializer_class = serializers.CreateRecordsSerializer

    def get_queryset(self):
        '''Return objects for the current authenticated user only'''
        queryset = self.queryset
        return queryset

    def perform_create(self, serializer):
        '''Create cleaning records and save the folder name to database for a Ride Share Driver'''
        FolderName = serializer.validated_data['folder_name']
        UberCleaningRecordBuilder.UberCleaningRecordBuilder.execRecordBuilderFunctionality(self, FolderName)
        #serializer.save()
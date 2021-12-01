from rest_framework import serializers
from core.models import UberDriver, CreateCleaningRecords

class UberDriverSerializer(serializers.ModelSerializer):
    '''Serializer for Uber Driver Objects'''

    class Meta:
        model = UberDriver
        fields = ('driver_id', 'driver_first_name', 'driver_last_name', 'driver_email')
        read_only_fields = ('driver_id',)

class CreateRecordsSerializer(serializers.ModelSerializer):
    '''Serializer for Creating Records Objects'''

    class Meta:
        model = CreateCleaningRecords
        fields = ('folder_id', 'folder_name')
        read_only_fields = ('folder_id',)

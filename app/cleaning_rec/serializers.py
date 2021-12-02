from django.db.models import fields
from rest_framework import serializers
from core.models import UberDriver, CreateCleaningRecords, UberCleaningRecords

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

class TransferCleaningRecordsSerializer(serializers.ModelSerializer):
    '''Serializer to transfer the cleaning records to main tables in database'''

    class Meta:
        model = UberCleaningRecords
        fields = ('id', 'driver_id', 'driver_certificate_id', 'date_and_time_of_trip', 
                  'date_and_time_of_clean', 'passenger_high_touch_surfaces','driver_high_touch_surfaces')
        read_only_fields = ('id',)
from rest_framework import serializers
from core.models import UberDriver

class UberDriverSerializer(serializers.ModelSerializer):
    '''Serializer for Uber Driver Objects'''

    class Meta:
        model = UberDriver
        fields = ('driver_id', 'driver_first_name', 'driver_last_name', 'driver_email')
        read_only_fields = ('driver_id',)


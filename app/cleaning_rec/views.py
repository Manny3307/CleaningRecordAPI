from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from core.models import UberDriver
from cleaning_rec import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

class UberDriverViewSets(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    '''Manage Ingredient in the Database'''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = UberDriver.objects.all()
    serializer_class = serializers.UberDriverSerializer

    def get_queryset(self):
        '''Return objects for the current authenticated user only'''
        
        queryset = self.queryset
        return queryset

    def perform_create(self, serializer):
        '''Create a new tag'''
        serializer.save()

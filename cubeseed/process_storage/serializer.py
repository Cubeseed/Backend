from rest_framework import serializers
from .models import ProcessStorage, DispatchedStorage

class ProcessStorageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProcessStorage
        fields = '__all__'


class DispatchedStorageSerializer(serializers.ModelSerializer):

    class Meta:
        model = DispatchedStorage
        fields = '__all__'

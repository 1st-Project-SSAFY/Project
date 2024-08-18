from rest_framework import serializers
from .models import Firefighter, Firestation, Main

class FirestationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firestation
        fields = '__all__'
        read_only_fields = []

class FirefighterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firefighter
        fields = '__all__'
        read_only_fields = ['firestation',]
        
class MainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Main
        fields = '__all__'
        read_only_fields = ['firestation',]
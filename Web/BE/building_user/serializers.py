from rest_framework import serializers
from .models import BuildingManager
        
class BuildingManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingManager
        fields = '__all__'
        read_only_fields = ['building','firestation',]
from rest_framework import serializers
from .models import Building, Building_Floor, Bicon, Sprinkler
        
class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'
        read_only_fields = ['firestation']
        
class BuildingFloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building_Floor
        fields = '__all__'
        read_only_fields = ['building']
        
class BiconSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bicon
        fields = '__all__'
        read_only_fields = ['building_floor']
    
class SprinklerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprinkler
        fields = '__all__'
        read_only_fields = ['building_floor']
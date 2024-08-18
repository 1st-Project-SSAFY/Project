from rest_framework import serializers
from .models import Fire_Issue, Fire_Logs
        
class FireIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fire_Issue
        fields = '__all__'
        read_only_fields = ['building_id', 'sprinkler']
        
class FireLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fire_Logs
        fields = '__all__'
        read_only_fields = ['robot_id','fire_id']
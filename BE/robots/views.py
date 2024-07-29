from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.serializers import serialize
from faker import Faker
import os
import requests
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from accounts.models import Firestation
from accounts.serializers import FirestationSerializer
from .models import Robot
from .serializers import RobotSerializer
from buildings.models import Building
from buildings.serializers import BuildingSerializer

###################### Fake Data ######################
@api_view(['GET'])
def fake_robots(request):
    fake = Faker('ko-KR')
    i = 0
    for buildings in Building.objects.all():
        building_serializer = BuildingSerializer(buildings)
        i += 1
        robot_id = 'ROBOT' + str(i)
        charged_state = 100
        battery = 100
        guide_liquid = 100
        right = True
        state = True
        start_x = 1
        start_y = 1
        min_floor = building_serializer.data.get('min_floor')
        max_floor = building_serializer.data.get('max_floor')
        for floor in range(min_floor, max_floor+1):
            save_data = {
                'robot_id':robot_id,
                'charged_state':charged_state,
                'battery':battery,
                'guide_liquid':guide_liquid,
                'right':right,
                'state':state,
                'location_floor':floor,
                'start_x':start_x,
                'start_y':start_y,
            }
            serializer = RobotSerializer(data=save_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(building_id=buildings)
    context = {
        'massage': 'Robot Data Save-Success'
    }
    return Response(context, status=status.HTTP_201_CREATED)

### 등록할때 사용하면 좋을 듯
def robot_id():
    return len(Robot.objects.all())
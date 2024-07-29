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
from .models import Building, Building_Floor, Sprinkler
from .serializers import BuildingSerializer, BuildingFloorSerializer, SprinklerSerializer

###################### Check Building ######################
@authentication_classes([TokenAuthentication])
@api_view(['GET'])
def check_building(request):
    buildings = Building.objects.filter(firestation = request.user.firestation)
    building_serializer = BuildingSerializer(buildings, many=True)
    building_lst = []
    for building in building_serializer.data:
        building_lst.append(building)
    context = {
        "count_building":len(building_lst),
        "building_list":building_lst
    }
    return Response(context, status = status.HTTP_200_OK)


###################### Fake Data ######################
## Building
API_KEY = settings.ADDRESS_API_KEY
BASE_URL = 'https://dapi.kakao.com/v2/local/search'

# fake building 생성
@api_view(['GET'])
def fake_building(request):
    fake = Faker('ko-KR')
    message = []
    headers = {
        'Authorization': f'KakaoAK {API_KEY}'
    }
    option = ['MT1','SC4','SW8','BK9','CT1','PO3','HP8']
    for firestation_ in Firestation.objects.all():
        firestation_serializer = FirestationSerializer(firestation_)
        station_name = firestation_serializer.data.get('firestation_name')
        x = firestation_serializer.data.get('firestation_x')
        y = firestation_serializer.data.get('firestation_y')
        for category in option:
            params = {
                'category_group_code': category,
                # 소방서 위치
                'x': x,
                'y': y,
                # 반경 1km내 검색
                'radius': 1000
            }
            response = requests.get(BASE_URL+'/category.json', headers=headers, params=params).json()
            for building in response.get('documents'):
                building_id = building.get('id')
                building_name = building.get('place_name')
                address = building.get('road_address_name'),
                min_floor = fake.pyint(min_value=-3, max_value=1)
                if min_floor == 0:
                    min_floor = 1
                max_floor = fake.pyint(min_value=1, max_value=10)
        
                if Building.objects.filter(building_id=building_id).exists():
                    continue
                if address[0] == '':
                    continue
                save_building = {
                    'building_id':building_id,
                    'building_name':building_name,
                    'address':address[0],
                    'min_floor':min_floor,
                    'max_floor':max_floor
                }
                serializer = BuildingSerializer(data=save_building)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(firestation=firestation_)
    
            message.append({
                'message':f'{station_name} {category} Data Save-Success'
            })
    
    return Response(message, status=status.HTTP_201_CREATED)

## Building Floor
@api_view(['GET'])
def fake_building_floor(request):
    for buildings in Building.objects.all():
        building_serializer = BuildingSerializer(buildings)
        b_name = building_serializer.data.get('building_name')
        min_floor = building_serializer.data.get('min_floor')
        max_floor = building_serializer.data.get('max_floor')
        for floor in range(min_floor, max_floor+1):
            if floor != 0:
                building_floor = b_name + '-'+floor
                img = '/home/ubuntu/file_data/building_images/mulcam_07.png'
                
                save_data = {
                    'building_floor':building_floor,
                    'floor':floor,
                    'img':img
                }
                serializer = BuildingFloorSerializer(data=save_data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(building=buildings)
    context = {
        'massage': 'Building_Floor Data Save-Success'
    }
    return Response(context, status=status.HTTP_201_CREATED)
    
## Sprinkler
@api_view(['GET'])
def fake_sprinkler(request):
    for building_floor in Building_Floor.objects.all():
        bf_serializer = BuildingFloorSerializer(building_floor)
        bf = bf_serializer.data.get('building_floor')
        sprinkler_id = bf + '-01' 
        save_data = {
            'sprinkler_id':sprinkler_id,
            'sprinkler_x':11,
            'sprinkler_y':17
        }
        serializer = SprinklerSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(building_floor=building_floor)
    context = {
        'massage': 'Sprinkler Data Save-Success'
    }
    return Response(context, status=status.HTTP_201_CREATED)
            
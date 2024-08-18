from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.serializers import serialize
# from django.core.files.base import ContentFile
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from faker import Faker
import paho.mqtt.client as mqtt
import threading
import os
import requests
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
import paho.mqtt.client as mqtt
import json
import time
import datetime

from accounts.models import Firestation, Firefighter
from accounts.serializers import FirestationSerializer, FirefighterSerializer
from robots.models import Robot
from robots.serializers import RobotSerializer
from fireissues.models import Fire_Issue, Fire_Logs
from fireissues.serializers import FireIssueSerializer, FireLogsSerializer
from building_user.models import BuildingManager
from building_user.serializers import BuildingManagerSerializer
from .models import Building, Building_Floor, Sprinkler
from .serializers import BuildingSerializer, BuildingFloorSerializer, SprinklerSerializer
from Escape_MQTT import robot_escape

##### 카카오맵 API 키, BASE URL
API_KEY = settings.ADDRESS_API_KEY
BASE_URL = 'https://dapi.kakao.com/v2/local/search'

##### S3 이미지 파일 업로드 함수
def upload_to_s3(file):
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name='ap-northeast-2'
    )
    
    object_name = 'building_image/' + file.name
    try:
        s3.head_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=object_name)
        file_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{object_name}"
        return file_url
    except ClientError:
        s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, object_name)
        file_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{object_name}"
        return file_url
    except (NoCredentialsError, PartialCredentialsError) as e:
        print("Credentials not available:", e)
        return None
    

## 소방관 - 관할 건물 조회 / 건물 클릭 시 상세 조회 및 정보 확인
###################### Check Building ######################
@authentication_classes([TokenAuthentication])
@api_view(['GET'])
def check_building(request):
    buildings = Building.objects.filter(firestation = request.user.firestation).order_by('-fire')
    building_serializer = BuildingSerializer(buildings, many=True)
    building_lst = []
    for building in building_serializer.data:
        building_lst.append(building)
    context = {
        "count_building":len(building_lst),
        "building_list":building_lst
    }
    return Response(context, status = status.HTTP_200_OK)

# 소방관 - 관할 건물 선택
###################### Choose Building ######################
@authentication_classes([TokenAuthentication])
@api_view(['GET'])
def choose_building(request, pk):
    ### 건물 정보
    b_ = Building.objects.get(pk=pk)
    building = BuildingSerializer(b_).data
    building_id = building.get('building_id')
    building_name = building.get('building_name')
    address = building.get('address')
    min_floor = building.get('min_floor')
    max_floor = building.get('max_floor')
    building_info = {
        'building_id':building_id,
        'building_name':building_name,
        'address':address,
        'min_floor':min_floor,
        'max_floor':max_floor
    }
    ### 층별 로봇 정보
    robot_lst = []
    for floor in range(min_floor, max_floor+1):
        if floor != 0:
            # 층별 전체 로봇 수
            robot_cnt = 0
            # 층별 정상 작동 로봇 수
            right_cnt = 0
            r_ = Robot.objects.filter(building_id=pk, location_floor=floor)
            for robot in RobotSerializer(r_, many=True).data:
                state = robot.get("state")
                if state:
                    robot_cnt += 1
                    # 만일 정상 작동하고 있는 로봇이라면 정상 작동 로봇 수에 추가
                    if robot.get('right'):
                        right_cnt += 1
            robot_info = {
                'floor':floor,
                'right':right_cnt,
                # 층별 전체 로봇 수에서 정상 작동 로봇 수를 빼서 비정상 로봇 수 산정
                'wrong':robot_cnt-right_cnt
            }
            
            bf = Building_Floor.objects.get(building=pk, floor=floor)
            bf_s = BuildingFloorSerializer(bf).data
            # 층별 화재 여부 추가
            robot_info['fire'] = bf_s.get('fire')
            # 만일 층별 설명이 있다면 추가
            etc = bf_s.get('etc')
            if etc:
                robot_info['etc'] = etc
            robot_lst.append(robot_info)
    context = {
        'building':building_info,
        'robot':robot_lst
    }
    return Response(context, status=status.HTTP_200_OK)

# 소방관 - 층 선택  
###################### Choose Building Floor ######################
@authentication_classes([TokenAuthentication])
@api_view(['GET'])
def choose_building_floor(request, pk, floor):
    ### 층 정보
    bf = Building_Floor.objects.get(building=pk, floor=floor)
    bf_s = BuildingFloorSerializer(bf).data
    fire = bf_s.get("fire")
    floor_info = {
        "floor":floor,
        "fire":fire,
        "img":bf_s.get("img")
    }
    etc = bf_s.get("etc")
    if etc:
        floor_info["etc"] = etc
    ### robot 정보
    r = Robot.objects.filter(building_id=pk, location_floor=floor)
    r_s = RobotSerializer(r, many=True)
    robot_info = []
    for r_s_data in r_s.data:
        state = r_s_data.get("state")
        if state:
            robot_id = r_s_data.get("robot_id")
            battery = r_s_data.get("battery")
            guide_liquid = r_s_data.get("guide_liquid")
            right = r_s_data.get("right")
            x = r_s_data.get("start_x")
            y = r_s_data.get("start_y")
            robot = {
                "pk":r_s_data.get('id'),
                "robot_id":robot_id,  # 로봇 아이디
                "battery":battery,  # 배터리 잔량
                "guide_liquid":guide_liquid,  # 용액 잔량
                "right":right,  # 정상 상태 여부
                "location_x":x,
                "location_y":y    
            }
            if fire:
                ## 대기
                mission = 0
            else:
                ## 화재 상황 아님
                mission = -1
            robot['mission'] = mission
            robot_info.append(robot)
    ### sprinkler (화재가 발생한 층에만 표시)
    sprinkler_info = []
    f = Fire_Issue.objects.filter(building_id=pk, end_dt=None, fire_floor=floor)
    f_s = FireIssueSerializer(f, many=True)
    for f_s_data in f_s.data:
        sprinkler_id = f_s_data.get("sprinkler")
        s = Sprinkler.objects.get(pk=sprinkler_id)
        s_data = SprinklerSerializer(s).data
        sprinkler_x = s_data.get("sprinkler_x")
        sprinkler_y = s_data.get("sprinkler_y")
        sprinkler = {
            "sprinkler_id":sprinkler_id,
            "sprinkler_x":sprinkler_x,
            "sprinkler_y":sprinkler_y
        }
        sprinkler_info.append(sprinkler)
    info = {
        "floor_info":floor_info,
        "robot_info":robot_info
    }
    if sprinkler_info:
        info["sprinkler_info"] = sprinkler_info
    return Response(info, status=status.HTTP_200_OK)

# 로봇의 최적경로
###################### SSE 최적경로 ######################
def robot_escape_root(request, pk, floor):
    def robot_root_stream():
        print("로봇 최적경로 SSE를 시작합니다.")
        while True:
            try:
                for robot in robot_escape:
                    if robot['topic'] == f"escape-root/{pk}/{floor}/":
                        print("로봇 최적경로를 전송합니다.")
                        print(robot)
                        yield f"data: {json.dumps(robot['path'])}\n\n"
                        robot_escape.clear()
                    else:
                        yield ":\n\n"
                        time.sleep(3)
                else:
                    yield ":\n\n"
                    time.sleep(3)
            except:
                yield ":\n\n"
                time.sleep(3)
    return StreamingHttpResponse(robot_root_stream(), content_type='text/event-stream')


# 소방관 - 로봇 상세 정보
###################### Check Robot Info ######################
@authentication_classes([TokenAuthentication])
@api_view(['GET', 'PATCH'])
def check_robot(request, pk, floor, robot_pk):
    if request.method == 'GET':
        r_ = Robot.objects.get(pk=robot_pk)
        robot = RobotSerializer(r_).data
        robot['mission'] = -1
        return Response(robot, status=status.HTTP_200_OK)
    if request.method == "PATCH":
        robot = Robot.objects.get(pk=robot_pk)
        robot_state = {'state':False}
        serializer = RobotSerializer(robot, data=robot_state, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':"로봇 비활성화 완료"}, status=status.HTTP_200_OK)
        

# 소방관(관리직) - 화재 상황 기록
###################### Record Fire Issues ######################
@authentication_classes([TokenAuthentication])
@api_view(['PATCH'])
def record_fire_issue(request, pk):
    ### building 화재 여부 수정
    building = Building.objects.get(pk=pk)
    fire_data = {
        "fire":False
    }
    building_s = BuildingSerializer(building, data=fire_data, partial=True)
    if building_s.is_valid(raise_exception=True):
        building_s.save()
    ### building_floor 화재 여부 수정
    b_f = Building_Floor.objects.filter(building=pk, fire=True)
    for fire_building_floor in b_f:
        b_f_s = BuildingFloorSerializer(fire_building_floor, data=fire_data, partial=True)
        if b_f_s.is_valid(raise_exception=True):
            b_f_s.save()
    ### Fire_Issue
    file_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/fire_video/{pk}/"
    dt = request.data.get('end_dt')
    fire_data = {
        # 화재 진압 일시
        "end_dt": datetime.datetime.strptime(request.data.get('end_dt'), "%Y-%m-%d %H:%M"),
        # 화재 규모(1~10)
        "fire_scale": request.data.get("fire_scale"),
        # 화재 현장 및 화재 발생 상세 설명
        "detail": request.data.get("detail"),
        # 현장 녹화 영상(로봇)
        "video": file_url
    }
    f_models= Fire_Issue.objects.filter(building_id=pk, end_dt=None).order_by('fire_dt')
    for fire_issues in f_models:
        serializer = FireIssueSerializer(fire_issues, data=fire_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    context = {
        "message":"화재 상황 정보 등록이 완료되었습니다."
    }
    return Response(context, status=status.HTTP_200_OK)


# 소방관(관리직) - 건물 관리자 등록
###################### Register Building Manager ######################
@authentication_classes([TokenAuthentication])
@api_view(['GET','POST', 'PATCH'])
def register_manager(request, pk):
    #### 관리자 여부 확인 및 생성 의사 재확인
    if request.method == 'GET':
        building_manager = BuildingManager.objects.filter(building=pk)
        building = Building.objects.get(pk=pk)
        building_data = BuildingSerializer(building).data
        id = building_data.get("building_id")
        if building_manager.exists():
            context = {
                "message":"해당 건물에 관리자 계정이 이미 있습니다.",
                "manager" :{
                    "id":"B-"+id,
                },
                "status":1,
            }
        else:
            fake = Faker()
            check_pw = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
            context = {
                "message":"관리자 계정을 생성하시겠습니까?\n 관리자 계정은 건물별로 하나만 생성 가능합니다",
                "manager":{
                    "id":"B-"+id,
                    "pw":check_pw,
                },
                "status":0,  
            }
        return Response(context, status=status.HTTP_200_OK)
    #### 관리자 계정 생성
    if request.method == 'POST':
        building = Building.objects.get(pk=pk)
        username = request.data.get("id")
        check_password = request.data.get("pw")
        password = make_password(check_password)
        manager = {
            "username":username,
            "password":password,
        }
        serializer = BuildingManagerSerializer(data=manager)
        if serializer.is_valid(raise_exception=True):
            print(check_password)
            serializer.save(building=building)
        context = {
            "message":"관리자 등록을 완료했습니다.",
            "manager":{
                "id":username,
                "pw":check_password,   
            }
        }
        return Response(context, status=status.HTTP_200_OK)
    #### 관리자 계정 비밀번호 재설정
    if request.method == 'PATCH':
        building_manager = BuildingManager.objects.get(building=pk)
        fake = Faker()
        remake_pw = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
        save_pw = make_password(remake_pw)
        data = {
            "password": save_pw
        }
        manager_serializer = BuildingManagerSerializer(building_manager, data=data, partial=True)
        if manager_serializer.is_valid(raise_exception=True):
            manager_serializer.save()
            context = {
                'message':"비밀번호 재설정 완료",
                'id': manager_serializer.data.get('username'),
                'pw': remake_pw
            }
            return Response(context, status=status.HTTP_200_OK)




# 소방관(관리직) - 건물 등록
###################### Building Register ######################
@authentication_classes([TokenAuthentication])
@api_view(['GET','POST'])
def building_register(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        buildings = []
        headers = {
            'Authorization': f'KakaoAK {API_KEY}'
        }
        params = {
            'query': query
        }
        response = requests.get(BASE_URL+'/keyword.json', headers=headers, params=params).json()

        for building in response.get('documents'):
            building_id = building.get('id')
            building_name = building.get('place_name')
            address = building.get('road_address_name')
            longitude = building.get('x')
            latitude = building.get('y')
            building_list = {
                'building_id':building_id,
                'building_name':building_name,
                'address':address,
                "longitude":longitude,
                "latitude":latitude
            }
            buildings.append(building_list)
        context = {
            'message': f'{query} 검색 결과입니다.',
            'building': buildings
        }
        return Response(context, status=status.HTTP_200_OK)
    if request.method == 'POST':
        user = Firefighter.objects.get(username = request.user.username)
        firefighter = FirefighterSerializer(user).data
        building_id = request.data.get('building_id')
        building_name = request.data.get("building_name")
        address = request.data.get("address")
        min_floor = request.data.get("min_floor")
        max_floor = request.data.get("max_floor")
        longitude = request.data.get("longitude")
        latitude = request.data.get("latitude")
        firestation = Firestation.objects.get(pk=firefighter.get('firestation'))
        
        if Building.objects.filter(building_id=building_id).exists():
            context = {'message': '이미 존재하는 건물입니다. 다른 소방서 관할 건물인지 확인하세요.'}
            return Response(context, status = status.HTTP_204_NO_CONTENT)
        if address == '':
            context = {'message': '주소가 존재하지 않는 건물입니다. 올바르게 입력했는지 확인하세요.'}
            return Response(context, status = status.HTTP_204_NO_CONTENT)
        save_building = {
            'building_id':building_id,
            'building_name':building_name,
            'address':address,
            'min_floor':min_floor,
            'max_floor':max_floor,
            "longitude":longitude,
            "latitude":latitude
        }
        serializer = BuildingSerializer(data=save_building)
        if serializer.is_valid(raise_exception=True):
            serializer.save(firestation=firestation)
        context= {
            'message':f'{building_name}이 성공적으로 등록되었습니다.'
        }    
        return Response(context, status=status.HTTP_200_OK)
# 소방관(관리직) - 건물 층 등록
###################### Building-Floor Register ######################
@authentication_classes([TokenAuthentication])
@api_view(['POST'])
def building_floor_register(request):
    building_id = request.data.get('building_id')
    b_ = Building.objects.get(building_id=building_id)
    building = BuildingSerializer(b_)
    min_floor = building.data.get('min_floor')
    max_floor = building.data.get('max_floor')
    
    context = []
    
    for floor in range(min_floor, max_floor+1):
        if floor != 0:
            file = request.FILES[f'image {floor}']
            file_ = file.read()
            file_url = upload_to_s3(file)
            etc = request.data.get(f'etc {floor}')
            if file_url:
                building_floor = building_id + 'F' + str(floor)
                img = ContentFile(file_, name=file.name)
                save_data = {
                    'building_floor':building_floor,
                    'floor':floor,
                    'img':img
                }
                if etc:
                    save_data['etc'] = etc
                if Building_Floor.objects.filter(building_floor=building_floor).exists():
                    continue
                serializer = BuildingFloorSerializer(data=save_data)
                print(save_data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(building=b_)
                    context.append({
                        'message': f'{building.data.get("building_name")}의 {floor}층 등록이 완료되었습니다.'
                    })
    return Response(context, status=status.HTTP_201_CREATED)









###################### Fake Data ######################
## Building
# fake building 생성
@api_view(['POST'])
def fake_building(request):
    fake = Faker('ko-KR')
    context = []
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
                address = building.get('road_address_name')
                longitude = building.get('x')
                latitude = building.get('y')
                min_floor = fake.pyint(min_value=-3, max_value=1)
                if min_floor == 0:
                    min_floor = 1
                max_floor = fake.pyint(min_value=1, max_value=10)
        
                if Building.objects.filter(building_id=building_id).exists():
                    continue
                if address == '':
                    continue
                if address[0] == '':
                    continue
                save_building = {
                    'building_id':building_id,
                    'building_name':building_name,
                    'address':address,
                    'min_floor':min_floor,
                    'max_floor':max_floor,
                    "longitude":longitude,
                    "latitude":latitude
                }
                serializer = BuildingSerializer(data=save_building)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(firestation=firestation_)
    
            context.append({
                'message':f'{station_name} {category} Data Save-Success'
            })
    
    return Response(context, status=status.HTTP_201_CREATED)

## Building Floor
@api_view(['POST'])
def fake_building_floor(request):
    # 이미지 파일을 요청에서 가져오기

    file = request.FILES['image']
    file_ = file.read()
    file_url = upload_to_s3(file)

    if file_url:
        for buildings in Building.objects.filter(firestation=2):
            building_serializer = BuildingSerializer(buildings)
            b_name = building_serializer.data.get('building_id')
            min_floor = building_serializer.data.get('min_floor')
            max_floor = building_serializer.data.get('max_floor')
            for floor in range(min_floor, max_floor+1):
                if floor != 0:
                    building_floor = b_name + 'F' + str(floor)
                    img = ContentFile(file_, name=file.name)
                    
                    save_data = {
                        'building_floor':building_floor,
                        'floor':floor,
                        'img':img
                    }
                    if Building_Floor.objects.filter(building_floor=building_floor).exists():
                        continue
                    serializer = BuildingFloorSerializer(data=save_data)
                    print(save_data)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save(building=buildings)
        context = {
            'message': 'Building_Floor Data Save-Success'
        }
        return Response(context, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Image upload failed.'}, status=status.HTTP_400_BAD_REQUEST)
    
## Sprinkler
@api_view(['POST'])
def fake_sprinkler(request):
    for building_floor in Building_Floor.objects.all():
        bf_serializer = BuildingFloorSerializer(building_floor)
        bf = bf_serializer.data.get('building_floor')
        sprinkler_id = bf + 'S01' 
        save_data = {
            'sprinkler_id':sprinkler_id,
            'sprinkler_x':11,
            'sprinkler_y':17
        }
        if Sprinkler.objects.filter(sprinkler_id=sprinkler_id).exists():
            continue
        serializer = SprinklerSerializer(data=save_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(building_floor=building_floor)
    context = {
        'message': 'Sprinkler Data Save-Success'
    }
    return Response(context, status=status.HTTP_201_CREATED)


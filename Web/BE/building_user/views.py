from django.shortcuts import render
from rest_framework.decorators import authentication_classes, api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from buildings.models import Building, Building_Floor
from buildings.serializers import BuildingSerializer, BuildingFloorSerializer
from robots.models import Robot
from robots.serializers import RobotSerializer
from .authentication import BuildingManagerTokenAuthentication

from rest_framework.permissions import IsAuthenticated

### 건물 관리자 - 건물 조회
@api_view(['GET'])
@authentication_classes([BuildingManagerTokenAuthentication])
def building(request):
    b_ = request.user.building
    ### 건물 정보
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
            r_ = Robot.objects.filter(building_id=b_, location_floor=floor)
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
            
            bf = Building_Floor.objects.get(building=b_, floor=floor)
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
        'robot':robot_lst,
    }
    return Response(context, status=status.HTTP_200_OK)


### 건물 관리자 - 층별 정보
@api_view(['GET'])
@authentication_classes([BuildingManagerTokenAuthentication])
def building_floor(request, floor):
    ### 층 정보
    b_ = request.user.building
    bf = Building_Floor.objects.get(building=b_, floor=floor)
    bf_s = BuildingFloorSerializer(bf).data
    floor_info = {
        "floor":floor,
        "img":bf_s.get("img")
    }
    etc = bf_s.get("etc")
    if etc:
        floor_info["etc"] = etc
    
    ### 층별 로봇 정보
    ### robot 정보
    r = Robot.objects.filter(building_id=b_, location_floor=floor)
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
                "pk":r_s_data.get("id"),
                "robot_id":robot_id,  # 로봇 아이디
                "battery":battery,  # 배터리 잔량
                "guide_liquid":guide_liquid,  # 용액 잔량
                "right":right,  # 정상 상태 여부
                "location_x":x,
                "location_y":y    
            }
            robot_info.append(robot)
    info = {
        "floor_info":floor_info,
        "robot_info":robot_info
    }
    return Response(info, status=status.HTTP_200_OK)


### 건물 관리자 - 로봇 상세 정보
@api_view(['GET'])
@authentication_classes([BuildingManagerTokenAuthentication])
def building_floor_robot(request, floor, robot_pk):
    r_ = Robot.objects.get(pk=robot_pk)
    robot = RobotSerializer(r_)
    robot_info = {
        'robot_id':robot.data.get('robot_id'),
        'upload_day':robot.data.get('upload_day'),
        'battery':robot.data.get('battery'),
        'guide_liquid':robot.data.get('guide_liquid'),
        'right':robot.data.get('right'),
    }
    return Response(robot_info, status=status.HTTP_200_OK)
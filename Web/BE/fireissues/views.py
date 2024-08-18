from django.shortcuts import render
from django.http import StreamingHttpResponse
import time
import paho.mqtt.client as mqtt
import json
import threading
from rest_framework.decorators import api_view, authentication_classes
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import TokenAuthentication

from accounts.models import Firestation
from accounts.serializers import FirestationSerializer
from buildings.models import Sprinkler, Building, Building_Floor
from buildings.serializers import SprinklerSerializer, BuildingSerializer, BuildingFloorSerializer
from robots.models import Robot
from robots.serializers import RobotSerializer
from .models import Fire_Issue, Fire_Logs
from .serializers import FireIssueSerializer, FireLogsSerializer
from Robot_MQTT import sprinkler_data, robot_count_list, robot_state_list, robot_detail_list

from rest_framework.response import Response
from rest_framework import status

client = mqtt.Client()
client.connect("3.36.55.201", 1883)


###################### 화재 발생 시 팝업 SSE ######################
def fire_popup(request):
    # firestation_id = request.user.firestation_id
    def fire_issues_stream():
        print("화재가 발생했습니다. 화재 발생 팝업을 띄웁니다.")
        while True:
            try:
                from Robot_MQTT import sprinkler_data
                if sprinkler_data:
                    sprinkler_pk = sprinkler_data.pop(0)
                    s_ = Sprinkler.objects.get(pk=sprinkler_pk)
                    sprinkler = SprinklerSerializer(s_).data
                    sprinkler_id = sprinkler.get('sprinkler_id')
                    building_id = sprinkler_id.split('F')[0]
                    fire_floor = sprinkler_id.split('F')[1].split('S')[0]
                    
                    # if Building.objects.filter(building_id=building_id,firestation_id=firestation_id).exists():
                    if Building.objects.filter(building_id=building_id).exists():
                        fire_issue = {
                            'fire_floor':int(fire_floor),
                            'fire_x':sprinkler.get('sprinkler_x'),
                            'fire_y':sprinkler.get('sprinkler_y')
                        }   
                        
                        ### building 화재 여부 수정
                        building = Building.objects.get(building_id=building_id)
                        fire_data = {
                            "fire":True
                        }
                        building_s = BuildingSerializer(building, data=fire_data, partial=True)
                        if building_s.is_valid(raise_exception=True):
                            building_s.save()
                            print(building_s.data)
                        ### building_floor 화재 여부 수정
                        b_f = Building_Floor.objects.get(building_floor = sprinkler_id.split('S')[0])
                        b_f_s = BuildingFloorSerializer(b_f, data=fire_data, partial=True)
                        if b_f_s.is_valid(raise_exception=True):
                            b_f_s.save()
                        
                        serializer = FireIssueSerializer(data=fire_issue)
                        if serializer.is_valid(raise_exception=True):
                            serializer.save(building_id=building, sprinkler=s_)
                        building_name = building_s.data.get('building_name')
                        building_info = {
                            "building_pk": building.pk,
                            "building_name": building_name,
                            "fire_floor": fire_floor
                        }
                        print("-----------------------------------화재 발생-----------------------------------")
                        yield f"data: {json.dumps(building_info)}\n\n"
                yield ":\n\n"
                time.sleep(5)
            except Exception as e:
                print(f"Error in fire_issues_stream: {e}")
                yield ":\n\n"
                time.sleep(5)
    return StreamingHttpResponse(fire_issues_stream(), content_type='text/event-stream')


### 건물 정상 로봇 갯수 확인
def robot_count(request, pk):
    b_ = Building.objects.get(pk=pk)
    r_ = Robot.objects.filter(building_id=b_)
    robot_id = []
    for robot in RobotSerializer(r_.only('robot_id'), many=True).data:
        robot_id.append(robot.get('robot_id'))
    if not BuildingSerializer(b_).data.get('fire'):
        client.publish("count_robot/", json.dumps(robot_id))
        print("로봇에게 MQTT 통신 성공")
        print(robot_id)
    def robot_count_stream():
        yield ":\n\n"
        print("건물의 로봇 상태를 확인하겠습니다. 값이 변경되면 로봇의 상태가 전송됩니다.")
        while True:
            try:
                from Robot_MQTT import robot_count_list
                if robot_count_list:
                    robot = robot_count_list.pop(0)
                    real_time_robot_id = robot.get('robot_id')
                    if real_time_robot_id in robot_id:
                        real_robot =r_.get(robot_id=real_time_robot_id)
                        # 층별 전체 로봇 수
                        robot_cnt = 0
                        # 층별 정상 작동 로봇 수
                        right_cnt = 0
                        floor = RobotSerializer(real_robot).data.get('location_floor')
                        floor_robot = Robot.objects.filter(building_id=b_, location_floor=floor)
                        for robot in RobotSerializer(floor_robot, many=True).data:
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
                        print("-----------------------------------floor, right, wrong-----------------------------------")
                        yield f"data: {json.dumps(robot_info)}\n\n"
                    else:
                        IndexError
                else:
                    IndexError
            except :
                yield ":\n\n"
                time.sleep(3)
    return StreamingHttpResponse(robot_count_stream(), content_type='text/event-stream')

### 층별 로봇 상태 확인
def robot_state(request, pk, floor):
    b_ = Building.objects.get(pk=pk)
    r_ = Robot.objects.filter(building_id=b_, location_floor=floor)
    robot_id = []
    for robot in RobotSerializer(r_.only('robot_id'), many=True).data:
        robot_id.append(robot.get('robot_id'))
    if not BuildingSerializer(b_).data.get('fire'):
        client.publish("count_robot/", json.dumps(robot_id))
        print("로봇에게 MQTT 통신 성공")
        print(robot_id)
    def fire_robot_stream():
        yield ":\n\n"
        print("층별 로봇 상태를 확인하겠습니다. 값이 변경되면 로봇의 상태가 전송됩니다.")
        while True:
            from Robot_MQTT import robot_state_list
            try:
                if robot_state_list:
                    robot = robot_state_list.pop(0)
                    if robot.get('robot_id') in robot_id:
                        print("-----------------------------------층별 robot 상태-----------------------------------")
                        yield f"data: {json.dumps(robot)}\n\n"
                    else:
                        IndexError
                else:
                    IndexError
            except IndexError:
                yield ":\n\n"
                time.sleep(3)
    return StreamingHttpResponse(fire_robot_stream(), content_type='text/event-stream')                    
                     
### 로봇 상세 정보 확인
def robot_detail(request, pk, floor, robot_pk):
    def robot_detail_stream():
        r = Robot.objects.get(pk=robot_pk)
        robot_serializer = RobotSerializer(r)
        robot = robot_serializer.data
        robot_id = robot.get('robot_id')
        mqtt_robot_id = [robot_id]
        
        b_ = Building.objects.get(pk=pk)
        if not BuildingSerializer(b_).data.get('fire'):
            client.publish("count_robot/", json.dumps(mqtt_robot_id))
        print("로봇 상세 정보를 확인하겠습니다. 값이 변경되면 로봇의 상태가 전송됩니다.")
        yield ":\n\n"
        while True:
            try:
                from Robot_MQTT import robot_detail_list
                if robot_detail_list:
                    robot = robot_detail_list.pop(0)
                    if robot.get('robot_id') == robot_id:
                        print("-----------------------------------robot 상세 정보-----------------------------------")
                        yield f"data: {json.dumps(robot)}\n\n"
                    else:
                        IndexError
                else:
                    IndexError
            except IndexError:
                yield ":\n\n"
                time.sleep(3)
    return StreamingHttpResponse(robot_detail_stream(), content_type='text/event-stream')


from buildings.models import Sprinkler, Building, Building_Floor
from buildings.serializers import SprinklerSerializer, BuildingSerializer, BuildingFloorSerializer
from robots.models import Robot
from robots.serializers import RobotSerializer
from fireissues.models import Fire_Issue, Fire_Logs
from fireissues.serializers import FireIssueSerializer, FireLogsSerializer
import paho.mqtt.client as mqtt
import json
import threading

sprinkler_data = []
robot_count_list = []
robot_state_list = []
robot_detail_list = []

def on_connect(client, userdata, flags, rc):
    client.subscribe("fire_issue/sprinkler/")
    print("fire_issue/sprinkler/ Connected !")
    client.subscribe("fire_issue/robots/#")
    print("fire_issue/robots/# Connected !")
    
def on_message(client, userdata, msg):
    global sprinkler_data
    global robot_count_list
    global robot_state_list
    global robot_detail_list

    topic = msg.topic
    if topic == "fire_issue/sprinkler/":
        context = msg.payload.decode("utf-8")
        sprinkler_data.append(context)
        print("fire_issue/sprinkler/ Received message !")
        ### 작동한 sprinkler가 있는 빌딩 내 모든 로봇 아이디 정보를 work_robot/으로 전송 
        ### -> 보낸 robot_id에 해당하는 로봇은 정보를 전송해줘!
        publish_robot_id = []
        sprinkler = Sprinkler.objects.get(pk=context)
        building_floor = SprinklerSerializer(sprinkler).data.get('building_floor')
        building_floor = Building_Floor.objects.get(pk=building_floor)
        building = BuildingFloorSerializer(building_floor).data.get('building')
        r_ = Robot.objects.filter(building_id=building)
        robots = RobotSerializer(r_, many=True).data
        for robot in robots:
            publish_robot_id.append(robot.get('robot_id'))
        client.publish("work_robot/", json.dumps(publish_robot_id))
        print("work_robot/ Send message !")
    else:
        print("로봇 데이터를 mqtt로 전송받았습니다.")
        context = msg.payload.decode("utf-8")
        context = json.loads(context)
        robot_id = context.get('robot_id')
        robot_info = context.get('info')
        robot_id = Robot.objects.get(robot_id=robot_id)
        robot_s = RobotSerializer(robot_id)
        building_id = robot_s.data.get('building_id')
        
        ## Robot에 로봇별로 저장
        battery = robot_info.get('battery')
        guide_liquid = robot_info.get('guide_liquid')
        if battery <= 10 or guide_liquid <= 20:
            right = False
        else:
            right = True
        robot_info_ = {
            'battery':battery,
            'guide_liquid':guide_liquid,
            'right':right,
        }
        serializer = RobotSerializer(robot_id, data=robot_info_, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        print("fire_issue/robots/# Robot Data Save !")
        
        try:
            fire_id= Fire_Issue.objects.filter(building_id=building_id, end_dt=None).order_by('-fire_dt')[0]
            # Fire_Logs에 로봇별로 log 저장
            serializer = FireLogsSerializer(data=robot_info)
            if serializer.is_valid(raise_exception=True):
                serializer.save(robot_id=robot_id, fire_id=fire_id)
            print("fire_issue/robots/# Fire_Logs Data Save !")
        except IndexError:
            pass
        
        # Robots 데이터 실시간 전송
        print('-------------------context확인---------------------')
        context['info']['right']=right
        robot_count_list.append(context)
        robot_state_list.append(context)
        robot_detail_list.append(context)

        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("3.36.55.201", 1883)

mqtt_thread = threading.Thread(target=client.loop_start, daemon=True)
mqtt_thread.start()
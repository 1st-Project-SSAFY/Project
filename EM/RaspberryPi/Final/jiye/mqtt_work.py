import paho.mqtt.client as mqtt
import json
import time
    
broker_address = "3.36.55.201"
pi = mqtt.Client("Pi")
pi.connect(broker_address, 1883)
pi.publish('destination/arrive/', "start")
while True:
    print("Work success")
    file_path1 = '/home/a204/jiye/servo_guide_liquid.json'
    value1=0
    # JSON 파일 읽기
    with open(file_path1, 'r', encoding='utf-8') as file1:
        data = json.load(file1)
        value1 = data
    file_path2 = '/home/a204/jiye/x120x/battery_capacity.json'
    value2=0
    # JSON 파일 읽기
    with open(file_path2, 'r', encoding='utf-8') as file2:
        data = json.load(file2)
        value2 = data
    file_path3 = '/home/a204/qdrive/real_test/robot_data.json'
    value_mission=0
    value_location_x=0
    value_location_y=0
    value_block_x=0
    value_block_y=0
    '''
    {
    "info": {
        "mission": "working",
        "location_x": 2,
        "location_y": 7,
        
        "block_x": 2,
        "block_y": 6
    }
}'''
    # JSON 파일 읽기
    with open(file_path3, 'r', encoding='utf-8') as file3:
        data = json.load(file3)
        value_mission=data["info"]["mission"]
        value_location_x=data["info"]["location_x"]
        value_location_y=data["info"]["location_y"]
        value_block_x=data["info"]["block_x"]
        value_block_y=data["info"]["block_y"]
    # 수정하기
    context = {
        'robot_id':'ROBOT5632',
        'info':{
            'battery':value2,
            'guide_liquid':value1,
            'mission':value_mission,
            'location_x':value_location_x,
            'location_y':value_location_y,
            ## 밑 항목은 장애물이 있을 때에만 보내주세요.
            'block_x':value_block_x,
            'block_y':value_block_y
        }
    }
    
    context = json.dumps(context)
    pi.publish('fire_issue/robots/ROBOT5632', context)
    if value_mission==2:
        print("stop work")
        time.sleep(5)
        pi.publish('destination/arrive/', "stop")
        time.sleep(10)
        break
    time.sleep(5)




'''
#subcriber code 

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected!")
    client.subscribe("ultrasonic/detect/object")
    
def on_message(client, userdata, msg):
    distance = float(msg.payload)
    print(f"distance: {distance}")

broker_address = "3.36.55.201"
pi = mqtt.Client("Pi")
pi.on_connect = on_connect
pi.on_message = on_message

pi.connect(broker_address, 1883)
pi.loop_forever()
'''

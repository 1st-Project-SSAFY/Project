import paho.mqtt.client as mqtt
import json
import time
def on_connect(client, userdata, flags, rc):
    print("Connected!")
    client.subscribe("count_robot/")
robots_list = [] 
def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    
        # Convert the JSON string to a Python list
    global robots_list 
    robots_list = json.loads(message)
    print(robots_list)
    

broker_address = "3.36.55.201"
pi = mqtt.Client("Pi")

'''pi.connect(broker_address, 1883)
pi.on_connect = on_connect
pi.on_message = on_message
pi.loop_start()'''
pi.connect(broker_address, 1883)
pi.on_connect = on_connect
pi.on_message = on_message
pi.loop_start()
value2 = 0
value2_copy = 0
while True:
    
    #print(robots_list)
    if 'ROBOT5632' in robots_list:
       # print(robots_list)
        #print("su")
        # JSON 파일 경로
        file_path1 = '/home/a204/jiye/servo_guide_liquid.json'
        value1=0
        # JSON 파일 읽기
        with open(file_path1, 'r', encoding='utf-8') as file1:
            data = json.load(file1)
            value1 = data
        file_path2 = '/home/a204/jiye/x120x/battery_capacity.json'
        #value2=0
        #value2_copy = 0
        # JSON 파일 읽기
        with open(file_path2, 'r', encoding='utf-8') as file2:
            content = file2.read().strip()
            if content:
                data = json.loads(content)
                value2 = data
        if value2_copy != value2:
            context = {
            'robot_id':'ROBOT5632',
            'info':{
                'battery':value2,
                'guide_liquid':value1,
                }
            }
            context = json.dumps(context)
            print(context)
            pi.publish('fire_issue/robots/ROBOT5632', context)
            print("success")
            value2_copy = value2
        #time.sleep(10)
        
        
       # pi.publish("count_robot/", '')
pi.loop_stop()
pi.disconnect()

'''
context = {
    'robot_id':'ROBOT5632',
    'info':{
        'battery':배터리잔량,
        'guide_liquid':액체잔량,
    }
}
context = json.dumps(context)
client.publish('fire_issue/robots/ROBOT5632', context)
'''
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

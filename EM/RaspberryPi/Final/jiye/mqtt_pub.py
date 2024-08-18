import paho.mqtt.client as mqtt
import json

# 브로커의 IP 주소와 포트 설정
broker_ip = "3.36.55.201"  # 특정 IP 주소를 입력
port = 1883  # 기본 MQTT 포트는 1883

# 발행할 토픽과 메시지 설정
publish_topic = "work_robot/"  # 발행할 토픽
data_list = ['ROBOT447', 'ROBOT5632','ROBOT448', 'ROBOT449', 'ROBOT450', 'ROBOT451', 'ROBOT452']  # 발행할 메시지
message = json.dumps(data_list)

'''# 구독할 토픽 설정
subscribe_topic = 'fire_issue/robots/ROBOT5632'  # 구독할 토픽
#subscribe_topic ='escape-root/818/10/'
'''
# MQTT 클라이언트 연결 성공 시 호출되는 콜백 함수
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.publish(publish_topic, message)  # 메시지 발행
        print(f"Message '{message}' published to topic '{publish_topic}'.")
        
        '''client.subscribe(subscribe_topic)  # 구독할 토픽 설정
        print(f"Subscribed to topic '{subscribe_topic}'")
    else:
        print("Connection failed with code ", rc)

# MQTT 메시지를 수신할 때 호출되는 콜백 함수
def on_message(client, userdata, msg):
    print(f"Message received from topic '{msg.topic}': {msg.payload.decode()}")
'''
# MQTT 클라이언트 초기화
client = mqtt.Client("PublisherClient")
client.on_connect = on_connect
#client.on_message = on_message

# 브로커에 연결
client.connect(broker_ip, port)

# 메시지 루프 시작
client.loop_forever()

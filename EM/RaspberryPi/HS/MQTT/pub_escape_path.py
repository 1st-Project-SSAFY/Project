import paho.mqtt.client as mqtt
import json

def publish_json_data(client, topic, file_path):
    # JSON 파일 읽기
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # JSON 데이터 퍼블리시
    client.publish(topic, json.dumps(data))

def on_connect(client, userdata, flags, rc):
    print("Connected!")
    client.subscribe("818/10F/escape-root")
    
    # JSON 데이터 퍼블리시 함수 호출
    publish_json_data(client, "818/10F/escape-root", 'path.json')

if __name__ == "__main__":
    broker_address = "3.36.55.201"
    pi = mqtt.Client("Pi")
    pi.on_connect = on_connect
    pi.connect(broker_address, 1883)
    
    # 메시지 루프 시작
    pi.loop_forever()

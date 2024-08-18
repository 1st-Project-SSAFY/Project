import paho.mqtt.client as mqtt
import json
import threading
robot_escape = []
def on_connect(client, userdata, flags, rc):
    client.subscribe("escape-root/#")
    print("escape-root/# Connected !")
    
def on_message(client, userdata, msg):
    global robot_escape
    topic = msg.topic
    context = msg.payload.decode("utf-8")
    context = json.loads(context)
    context['topic'] = topic
    robot_escape.append(context)
    print("escape-root/# Data Subscribe Success !")
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("3.36.55.201", 1883)

mqtt_thread = threading.Thread(target=client.loop_start, daemon=True)
mqtt_thread.start()

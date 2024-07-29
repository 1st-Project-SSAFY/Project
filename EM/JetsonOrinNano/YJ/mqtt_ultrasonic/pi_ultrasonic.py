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
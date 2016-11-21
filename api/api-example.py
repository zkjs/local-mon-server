#-*- encoding=utf-8 -*-
#this is a example for demo how api thread works for local server
#ganben

from flask import Flask
import paho.mqtt.client as mqtt #for demo data flow of mqtt


app = Flask(__name__)

def on_publish(mosq, obj, mid):
    print('pub mid:{0}'.format(str(mid)))

mqttc = mqtt.Client('apipuber')
mqttc.on_publish = on_publish

mqttc.connect('192.168.1.100', 1883, 60)


@app.route('/')
def hello_data():
    mqttc.publish('position', 'this is a api position message')
    return 'hello data!'


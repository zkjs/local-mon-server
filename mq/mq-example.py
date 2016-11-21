#-*- encoding=utf-8 -*-
#a example to demo multi threading python app for mq handling
#ganben

import Queue
import threading
import time
import paho.mqtt.client as mqtt

queueLock = threading.Lock()
posiQueue = Queue.Queue(100)
callQueue = Queue.Queue(100)
threads = []
threadID = 1

def on_connect(client, userdata, rc):
    client.subscribe('position')
    client.subscribe('nursecall') #maybe here can be configured
    print('Connected with result code {0}'.format(str(rc)))

def on_message(client, userdata, msg):
    print('Topic={0}, Message={1}'.format(msg.topic, str(msg.payload)))
    if msg.topic == 'position':
        queueLock.acquire()
        posiQueue.put(str(msg.payload))
        queueLock.release()
    elif msg.topic == 'nursecall':
        queueLock.acquire()
        callQueue.put(str(msg.payload))
        queueLock.release()

class MqttListener(threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        process_data(self.name, self.q)
        print('exiting ... {0}'.format(self.name))

def process_data(threadName, q):
    while True:
        queueLock.acquire()
        if not q.empty():
            data = q.get()
            queueLock.release()
            print('get {0} by {1}'.format(data, threadName))
        else:
            queueLock.release()
        time.sleep(5)

#create threads
thread1 = MqttListener(1, 'thread1', posiQueue)
thread1.start()
threads.append(thread1)
thread2 = MqttListener(2, 'thread2', callQueue)
thread2.start()
threads.append(thread2)

#set up mqtt client
client = mqtt.Client('server-listener')
client.on_connect = on_connect
client.on_message = on_message

client.connect('192.168.1.100', 1883, 60)
client.loop_forever()


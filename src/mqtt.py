import random
import sys
import time

import paho.mqtt.client as mqtt
from ledstrip import LedStrip

class MqttListener:
    def __init__(self, led_strip):
        """
        :type led_strip: LedStrip
        """
        self.led_strip = led_strip

        self.host = "test.mosquitto.org"
        self.port = 1883
        client_id = "tek-" + str(random.randint(0, 1000000))

        self.client = mqtt.Client(client_id=client_id, clean_session=True)

        self.client.connected_flag = False
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message


    def connect(self):
        self.client.connect(self.host, self.port, keepalive=60)
        while not self.client.connected_flag:  # wait in loop
            self.client.loop()
            time.sleep(1)
        print("mqtt connected")

        self.client.subscribe("tek/staging/light/1/state")
        self.client.subscribe("tek/staging/light/1/brightness")
        print("subscribed")

        self.client.loop_forever()

    def __del__(self):
        if self.client:
            self.client.disconnect()

    def on_connect(self, client, userdata, flags, rc):
        """ Callback called when connection/reconnection is detected """
        print("Connect %s result is: %s" % (self.host, rc))

        if rc == 0:
            self.client.connected_flag = True
            print("connected OK")
            return

        print("Failed to connect to %s, error was, rc=%s" % rc)
        # handle error here
        sys.exit(-1)

    def on_message(self, client, userdata, msg):
        """ Callback called for every PUBLISH received """
        print("Message received")
        print(msg.payload.decode())
        print(msg.topic)
        if msg.topic == "tek/staging/light/1/state":
            self.led_strip.set_profile(msg.payload.decode())
            print("Topic %s matched" % msg.topic)
        elif msg.topic == "tek/staging/light/1/brightness":
            self.led_strip.set_brightness(int(msg.payload.decode()))
            print("Topic %s  matched" % msg.topic)
        else:
            print("Topic %s not matched"%msg.topic)


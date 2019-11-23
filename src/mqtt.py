import sys
import time

import paho.mqtt.client as mqtt
from ledstrip import LedStrip

class MqttListener:
    def __init__(self,led_strip):
        """

        :type led_strip: LedStrip
        """
        self.led_strip = led_strip

        self.host = "node02.myqtthub.com"
        self.port = 1883
        clean_session = True
        client_id = "raspi"
        user_name = "raspi"
        password = "bigboy"

        self.client = mqtt.Client(client_id=client_id, clean_session=clean_session)
        self.client.username_pw_set(user_name, password)
        # connect using standard unsecure MQTT with keepalive to 60

        self.client.connected_flag = False

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message


    def connect(self):
        self.client.connect(self.host, self.port, keepalive=60)
        while not self.client.connected_flag:  # wait in loop
            self.client.loop()
            time.sleep(1)
        print("mqtt connected")
        # publish message (optionally configuring qos=1, qos=2 and retain=True/False)
        ret = self.client.publish("some/message/to/publish", "{'status' : 'on'}")
        self.client.subscribe("some/profile")
        print("subscribed")
        self.client.loop_forever()



    def __del__(self):
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
        self.led_strip.set_profile(msg.payload.decode())
        print("%s => %s" % (msg.topi, msg.payload.decode()))
        # if msg.topi =="led_strip/profile":



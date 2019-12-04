import json
import random
import sys
import time

import paho.mqtt.client as mqtt
from ledstrip import LedStrip
from transitions import Sudden, Fade


class MqttListener:
    def __init__(self, led_strip):
        """
        :type led_strip: LedStrip
        """
        self.led_strip = led_strip

        self.host = "mqtt.eclipse.org"
        self.port = 1883
        client_id = "tek-" + str(random.randint(0, 10000000))

        self.client = mqtt.Client(client_id=client_id, clean_session=False)
        self.client.connected_flag = False
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def connect(self):
        self.client.connect(self.host, self.port, keepalive=60)
        while not self.client.connected_flag:  # wait in loop
            self.client.loop()
            time.sleep(1)
        print("mqtt connected")

        self.client.subscribe("tek/staging/light/1/#", qos=1)
        # self.client.subscribe("tek/staging/light/1/brightness")
        # self.client.subscribe("tek/staging/light/simulated")
        print("subscribed")

        self.client.loop_start()

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
        """
        Callback called for every PUBLISH received
        """
        topic = msg.topic.split("/")
        if len(topic) == 0:
            print("Invalid message, empty topic")
            return

        target = topic[-1]

        payload = json.loads(msg.payload.decode())

        if target == "state":
            self.handle_state_message(payload)
        elif target == "brightness":
            self.handle_brightness_message(payload)
        else:
            print("Error target %s not found" % target)

    def handle_brightness_message(self, payload):
        self.led_strip.transition.brightness = payload["brightness"]

    def handle_state_message(self, payload):
        params = payload["params"]
        transition_name = payload["transition"]

        if not transition_name:
            print("Something went wrong")
            return

        if transition_name == "sudden":
            print("Sudden mode activated")
            transition = Sudden(**params)
        elif transition_name == "fade":
            transition = Fade(**params)
        else:
            transition = Sudden(1.0, 0.0, 0.0)

        self.led_strip.transition = transition

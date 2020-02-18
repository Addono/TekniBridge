import json
import random
import sys
import time
from typing import List, Optional

import paho.mqtt.client as mqtt  # pyre-ignore

from bridges import AbstractLight
from transitions import Sudden, Fade, ThermalCycle, Wipe, Christmas, AbstractTransition


class MqttListener:
    def __init__(self, lights: List[AbstractLight]):
        self._lights = lights

        self.host = "test.mosquitto.org"
        self.port = 8081
        client_id = "tek-" + str(random.randint(0, 10000000))

        self.client = mqtt.Client(client_id=client_id, clean_session=False, transport="websockets")
        self.client.connected_flag = False
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.tls_set()

        self.brightness = 0
        self.transition_name = "sudden"
        self.transition_params = {"red": 1, "blue": 1, "green": 1}

    def connect(self):
        self.client.connect(self.host, self.port, keepalive=60)
        while not self.client.connected_flag:  # wait in loop
            self.client.loop()
            time.sleep(1)
        print("mqtt connected")

        self.client.subscribe("tek/staging/light/1/#", qos=1)
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
        self.brightness = payload["brightness"]

        for light in self._lights:
            light.transition.brightness = self.brightness

    def handle_state_message(self, payload):
        self.transition_name = payload["transition"].lower()
        self.transition_params = payload["params"]

        for light in self._lights:
            self.update_light(light)

    def add_light(self, light: AbstractLight):
        self._lights.append(light)
        self.update_light(light)

    def remove_light(self, light: AbstractLight):
        self._lights.remove(light)

    def get_lights(self):
        return self._lights

    def update_light(self, light: AbstractLight):
        # Create a new transition object from the payload
        transition = self.transition_builder()

        if transition:
            # Set the brightness of this new transition
            transition.brightness = self.brightness

            light.transition = transition
        else:

            print("Skip updating light as no transition object could be generated")

    def transition_builder(self) -> Optional[AbstractTransition]:
        if self.transition_name == "sudden" and self.transition_params:
            return Sudden(**self.transition_params)
        elif self.transition_name == "fade" and self.transition_params:
            return Fade(**self.transition_params)
        elif self.transition_name == "thermal_cycle":
            return ThermalCycle()
        elif self.transition_name == "wipe" and self.transition_params:
            return Wipe(**self.transition_params)
        elif self.transition_name == "christmas":
            return Christmas()

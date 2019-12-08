from yeelight import discover_bulbs

from bridges import RpiWs281xLedstrip, Yeelight
from mqtt import MqttListener

bulbs = discover_bulbs(timeout=10)

lights = [
    RpiWs281xLedstrip(),
    *(Yeelight.from_discover_bulbs_dict(bulb) for bulb in bulbs),
]

mqttlistener = MqttListener(lights)
mqttlistener.connect()

while True:
    for light in lights:
        light.control()

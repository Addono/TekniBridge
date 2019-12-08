from bridges import RpiWs281xLedstrip
from mqtt import MqttListener


ledstrip = RpiWs281xLedstrip()

mqttlistener = MqttListener([ledstrip])
mqttlistener.connect()

while True:
    ledstrip.control()

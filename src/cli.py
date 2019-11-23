from mqtt import MqttListener
from ledstrip import LedStrip


ledstrip = LedStrip()

mqttlistener = MqttListener(ledstrip)

mqttlistener.connect()


while True:
    a =0







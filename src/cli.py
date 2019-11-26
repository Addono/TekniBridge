from mqtt import MqttListener
from ledstrip import LedStrip

ledstrip = LedStrip()
while True:
    ledstrip.set_profile("cold")
mqttlistener = MqttListener(ledstrip)
ledstrip.pixel_strip.getPixels()

mqttlistener.connect()


while True:
    a =0







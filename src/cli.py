from mqtt import MqttListener
from ledstrip import LedStrip

ledstrip = LedStrip()
mqttlistener = MqttListener(ledstrip)
ledstrip.pixel_strip.getPixels()

mqttlistener.connect()


while True:
    a =0







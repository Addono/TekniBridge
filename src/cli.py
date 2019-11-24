from mqtt import MqttListener
from ledstrip import LedStrip

ledstrip = LedStrip()
while True:
    ledstrip.color_rand_appear(ledstrip.temp2rgb(1000))
    ledstrip.color_wipe(ledstrip.temp2rgb(30000),random_index=True)
mqttlistener = MqttListener(ledstrip)
ledstrip.pixel_strip.getPixels()

mqttlistener.connect()


while True:
    a =0







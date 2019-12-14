import sentry_sdk
sentry_sdk.init("https://4e23e9f9b616446582af0ce4fc3c7f53@sentry.io/1857022")

from multiprocessing import Queue
from threading import Thread

from yeelight import discover_bulbs

from bridges import RpiWs281xLedstrip, Yeelight
from mqtt import MqttListener


def discover_yeelights(lights_queue: Queue):
    # Track which ip addresses we already found
    discovered_bulbs = []

    while True:
        bulbs = discover_bulbs(timeout=10)
        for bulb in bulbs:
            ip = bulb["ip"]
            if ip not in discovered_bulbs:
                print("Found new bulb at %s" % ip)
                # Add the newly discovered bulb to our list of detected bulbs
                lights_queue.put(bulb)

                # Mark it as detected such that we won't add it the next time we find it
                discovered_bulbs.append(ip)


if __name__ == '__main__':
    lights = [RpiWs281xLedstrip()]

    # Create the connection to the MQTT server
    mqtt_listener = MqttListener(lights)
    mqtt_listener.connect()

    # Create a new process which scans for new Yeelights asynchronously
    new_lights_queue = Queue()
    yeelight_discoverer = Thread(target=discover_yeelights, args=(new_lights_queue,))
    yeelight_discoverer.start()

    while True:
        # See if any new Yeelights were discovered
        if not new_lights_queue.empty():
            bulb = Yeelight.from_discover_bulbs_dict(new_lights_queue.get())
            lights.append(bulb)

        # Give control to the lights
        for light in lights:
            try:
                light.control()
            except KeyboardInterrupt:
                pass  # Ignore keyboard interrupts
            except Exception as e:
                sentry_sdk.capture_exception(e)
                lights.remove(light)
                print("Exception found for light %s: %s" % (light, e))

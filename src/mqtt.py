import paho.mqtt.client as mqtt
import time
import ssl
import led_strip

host          = "node02.myqtthub.com"
port          = 1883
clean_session = True
client_id     = "raspi"
user_name     = "raspi"
password      = "bigboy"

def on_connect (client, userdata, flags, rc):
    """ Callback called when connection/reconnection is detected """
    print ("Connect %s result is: %s" % (host, rc))
    
    # With Paho, always subscribe at on_connect (if you want to
    # subscribe) to ensure you resubscribe if connection is
    # lost.
    client.subscribe("some/profile")

    if rc == 0:
        client.connected_flag = True
        print ("connected OK")
        return
    
    print ("Failed to connect to %s, error was, rc=%s" % rc)
    # handle error here
    sys.exit (-1)


def on_message(client, userdata, msg):
    """ Callback called for every PUBLISH received """
    #print ("%s => %s" % (msg.topi, str(msg.payload)))
    #if msg.topi =="led_strip/profile":
    led_strip.setProfile(msg.payload)
        

    

# Define clientId, host, user and password
client = mqtt.Client (client_id = client_id, clean_session = clean_session)
client.username_pw_set (user_name, password)

client.on_connect = on_connect
client.on_message = on_message

# configure TLS connection
# client.tls_set (cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)
# client.tls_insecure_set (False)
# port = 8883

# connect using standard unsecure MQTT with keepalive to 60
client.connect (host, port, keepalive = 60)
client.connected_flag = False
while not client.connected_flag:           #wait in loop
    client.loop()
    time.sleep (1)

# publish message (optionally configuring qos=1, qos=2 and retain=True/False)
ret = client.publish ("some/message/to/publish", "{'status' : 'on'}")
client.loop ()

print ("Publish operation finished with ret=%s" % ret)

# close connection
client.disconnect ()
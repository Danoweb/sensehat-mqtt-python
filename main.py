import os, time, json
from sense_hat import SenseHat
from dotenv import load_dotenv
from paho.mqtt import client as mqtt_client

load_dotenv()  # take environment variables from .env.

MACHINE_ID = os.getenv('DEVICE_ID')
UPDATE_SECONDS = int(os.getenv('UPDATE_SECONDS'))
MQTT_HOST = os.getenv('MQTT_HOST')
MQTT_PORT = 1883
MQTT_USERNAME = os.getenv('MQTT_USERNAME')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')

sense = SenseHat()
sense_data = {}

def connect_mqtt() -> mqtt_client:
    """Connects to MQTT Broker with Environment Configuration

    Returns:
        mqtt_client: mqtt_client in connected state
    """
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(MACHINE_ID)
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.connect(MQTT_HOST, MQTT_PORT)
    return client

def publish_sensor(client):
    """Publishes Sensor data to the MQTT Client Provided (Infinitely)

    Args:
        client (MQTTClient): MQTT Client Object with Connection State
    """
    #Get Sensor Data, Publish, Sleep until next update.
    while True:
        sense_temp = sense.get_temperature()
        sense_pressure = sense.get_pressure()
        sense_humidity = sense.get_humidity()
        #Convert to Farenheit
        sense_temp = ((sense_temp/5)*9)+32
        
        sense_data['sense_hat'] = {
            "temperature": round(sense_temp, 1),
            "pressure": round(sense_pressure, 1),
            "humidity": round(sense_humidity, 1),
        }

        msg = f"Temperature: {sense_data['sense_hat']['temperature']} Pressure: {sense_data['sense_hat']['pressure']} Humidity: {sense_data['sense_hat']['humidity']}"
        print(f"{msg}")
        #sense.show_message(msg, scroll_speed=0.05, back_colour=bg)
        
        publish_result = client.publish(topic=f"{MACHINE_ID}", payload=json.dumps(sense_data))
        print(f"PublishResult: {publish_result}")
        
        time.sleep(UPDATE_SECONDS)
    
    
def run():
    client = connect_mqtt()
    client.loop_start()
    publish_sensor(client)
    #client.loop_forever()


if __name__ == '__main__':
    run()
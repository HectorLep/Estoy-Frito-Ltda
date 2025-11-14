import paho.mqtt.client as mqtt
import json
import time
from generate_json import generate_sensor_data
from datetime import datetime

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "sensores"
MQTT_USERNAME = "publisher"
MQTT_PASSWORD = "pub123"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✓ Conectado al broker MQTT exitosamente")
    else:
        print(f"✗ Error de conexión. Código: {rc}")

def on_publish(client, userdata, mid):
    print(f"✓ Mensaje publicado (ID: {mid})")

client = mqtt.Client()
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_publish = on_publish

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    
    print("=" * 60)
    print(f"MQTT Publisher - Publicando en tópico '{MQTT_TOPIC}'")
    print(f"Broker: {MQTT_BROKER}:{MQTT_PORT}")
    print("=" * 60)
    
    while True:
        sensor_data = generate_sensor_data()
        message = json.dumps(sensor_data)
        
        result = client.publish(MQTT_TOPIC, message)
        
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
        print(f"  Temp: {sensor_data['dUMA']['environment']['temperature']}°C, Humedad: {sensor_data['dUMA']['environment']['humidity']}%, IAQ: {sensor_data['dUMA']['air_quality']['iaq_index']}")
        
        time.sleep(5)
        
except KeyboardInterrupt:
    print("\n\nPublicador detenido por el usuario")
    client.loop_stop()
    client.disconnect()
except Exception as e:
    print(f"\n✗ Error: {e}")
    client.loop_stop()
    client.disconnect()

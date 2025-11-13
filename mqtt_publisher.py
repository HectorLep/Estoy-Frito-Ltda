#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Publisher MQTT - Publica datos en el tópico 'sensores'
"""

import paho.mqtt.client as mqtt
import json
import time
from generate_json import generate_sensor_data

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "sensores"
MQTT_USERNAME = "publisher"
MQTT_PASSWORD = "pub123"
INTERVAL_SECONDS = 5

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("✓ Conectado al broker MQTT exitosamente")
    else:
        print(f"✗ Error de conexión. Código: {reason_code}")

def on_publish(client, userdata, mid, reason_code, properties):
    print(f"✓ Mensaje publicado (ID: {mid})")

if __name__ == "__main__":
    # Crear cliente MQTT con callback API version
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Publisher_SensorData")
    
    # Configurar credenciales
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    
    # Configurar callbacks
    client.on_connect = on_connect
    client.on_publish = on_publish
    
    print("=" * 60)
    print("MQTT Publisher - Publicando en tópico 'sensores'")
    print(f"Broker: {MQTT_BROKER}:{MQTT_PORT}")
    print("=" * 60)
    
    try:
        # Conectar al broker
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        
        while True:
            # Generar datos aleatorios
            sensor_data = generate_sensor_data()
            json_payload = json.dumps(sensor_data, ensure_ascii=False)
            
            print(f"\n[{sensor_data['dUMA']['timestamp']}]")
            print(f"  Temp: {sensor_data['dUMA']['environment']['temperature']}°C")
            
            # Publicar mensaje
            client.publish(MQTT_TOPIC, json_payload, qos=1)
            time.sleep(INTERVAL_SECONDS)
            
    except KeyboardInterrupt:
        print("\n\n✓ Publisher detenido")
        client.loop_stop()
        client.disconnect()

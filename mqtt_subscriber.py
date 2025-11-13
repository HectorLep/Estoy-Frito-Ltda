#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Subscriber MQTT - Se suscribe y reenvía a NodeRed
"""

import paho.mqtt.client as mqtt
import requests
import json

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "sensores"
MQTT_USERNAME = "subscriber"
MQTT_PASSWORD = "sub123"
NODERED_URL = "http://localhost:1880/sensor_data_mqtt"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✓ Conectado al broker MQTT")
        client.subscribe(MQTT_TOPIC, qos=1)
        print(f"✓ Suscrito al tópico: {MQTT_TOPIC}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f"\n✓ Mensaje recibido del tópico '{msg.topic}'")
        print(f"  Temp: {payload['dUMA']['environment']['temperature']}°C")
        response = requests.post(NODERED_URL, json=payload, headers={"Content-Type": "application/json"}, timeout=5)
        if response.status_code == 200:
            print(f"  → Reenviado a NodeRed exitosamente")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    client = mqtt.Client("Subscriber_SensorData")
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    
    print("=" * 60)
    print("MQTT Subscriber - Escuchando tópico 'sensores'")
    print("=" * 60)
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n\n✓ Subscriber detenido")
        client.disconnect()

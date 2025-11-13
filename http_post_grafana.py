#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para enviar datos JSON a Grafana vía HTTP POST
"""

import requests
import json
import time
from generate_json import generate_sensor_data

GRAFANA_URL = "http://localhost:3000/api/live/push/sensor_data"
GRAFANA_API_KEY = ""
INTERVAL_SECONDS = 5

def send_to_grafana(data):
    headers = {"Content-Type": "application/json"}
    if GRAFANA_API_KEY:
        headers["Authorization"] = f"Bearer {GRAFANA_API_KEY}"
    try:
        response = requests.post(GRAFANA_URL, json=data, headers=headers, timeout=5)
        if response.status_code in [200, 204]:
            print(f"✓ Datos enviados exitosamente a Grafana")
        else:
            print(f"✗ Error al enviar a Grafana: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Error de conexión con Grafana: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Enviando datos a Grafana vía HTTP POST")
    print("=" * 60)
    try:
        while True:
            sensor_data = generate_sensor_data()
            print(f"\n[{sensor_data['dUMA']['timestamp']}]")
            send_to_grafana(sensor_data)
            time.sleep(INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\n\n✓ Envío detenido")

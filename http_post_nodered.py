#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para enviar datos JSON a NodeRed vía HTTP POST
"""

import requests
import json
import time
from generate_json import generate_sensor_data

# Configuración de NodeRed
NODERED_URL = "http://localhost:1880/sensor_data"
INTERVAL_SECONDS = 5

def send_to_nodered(data):
    try:
        response = requests.post(
            NODERED_URL,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 200:
            print(f"✓ Datos enviados exitosamente a NodeRed")
        else:
            print(f"✗ Error al enviar a NodeRed: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Error de conexión con NodeRed: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Enviando datos a NodeRed vía HTTP POST")
    print(f"URL: {NODERED_URL}")
    print("=" * 60)
    print("Presiona Ctrl+C para detener\n")
    
    try:
        while True:
            sensor_data = generate_sensor_data()
            print(f"\n[{sensor_data['dUMA']['timestamp']}]")
            print(f"  Temp: {sensor_data['dUMA']['environment']['temperature']}°C, "
                  f"Humedad: {sensor_data['dUMA']['environment']['humidity']}%, "
                  f"IAQ: {sensor_data['dUMA']['air_quality']['iaq_index']}")
            send_to_nodered(sensor_data)
            time.sleep(INTERVAL_SECONDS)
            
    except KeyboardInterrupt:
        print("\n\n✓ Envío detenido por el usuario")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import time
from datetime import datetime 
from generate_json import generate_sensor_data

GRAFANA_URL = "http://localhost:3000/api/live/push/sensor_data"
GRAFANA_API_KEY = "" 
INTERVAL_SECONDS = 5

def send_to_grafana(data):
    temp = data['dUMA']['environment']['temperature']
    hum = data['dUMA']['environment']['humidity']
  
    linea_datos = f"sensores temperatura={temp},humedad={hum}"
    headers = {"Content-Type": "text/plain"}
    
    if GRAFANA_API_KEY:
        headers["Authorization"] = f"Bearer {GRAFANA_API_KEY}"
        
    try:
        response = requests.post(GRAFANA_URL, data=linea_datos, headers=headers, timeout=5)
        
        if response.status_code in [200, 204]:
            print(f"✓ Datos enviados exitosamente a Grafana")
        else:
            print(f"⚠ Grafana respondió: {response.status_code} (Probablemente falta configurar el Stream en Grafana)")
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Error de conexión: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Enviando datos a Grafana vía HTTP POST (Método Push)")
    print("=" * 60)
    try:
        while True:
            sensor_data = generate_sensor_data()
            hora_actual = datetime.now().strftime('%H:%M:%S')
            print(f"\n[{hora_actual}] Generando datos...")
            send_to_grafana(sensor_data)
            time.sleep(INTERVAL_SECONDS)
            
    except KeyboardInterrupt:
        print("\n\n✓ Envío detenido")
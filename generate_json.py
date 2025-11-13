#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para generar JSON con datos aleatorios de sensores ambientales
Proyecto #3 Interfaces Gráficas - INFO1128
Estoy Frito Ltda
"""

import random
import json
from datetime import datetime

def generate_sensor_data():
    """
    Genera un objeto JSON dUMA con datos aleatorios de sensores
    """
    data = {
        "dUMA": {
            "timestamp": datetime.now().isoformat(),
            "air_quality": {
                "iaq_index": random.randint(0, 250),
                "quality_label": random.choice(["good", "moderate", "poor", "unhealthy"]),
                "accuracy": random.randint(0, 3)
            },
            "environment": {
                "temperature": round(random.uniform(15.0, 30.0), 2),
                "humidity": round(random.uniform(25.0, 70.0), 2),
                "air_pressure": round(random.uniform(950.0, 1050.0), 2)
            },
            "stats": {
                "memory_usage_percent": random.randint(10, 90),
                "cpu_usage_percent": random.randint(10, 90),
                "logins": random.randint(0, 500),
                "server_requests": random.randint(100, 10000),
                "sign_ups": random.randint(0, 500),
                "logouts": random.randint(0, 300),
                "sign_outs": random.randint(0, 400)
            },
            "disk_usage": [
                {"partition": f"sda{i}", "usage_gb": random.randint(1, 100)}
                for i in range(1, 17)
            ]
        }
    }
    return data

if __name__ == "__main__":
    # Generar y mostrar JSON
    sensor_data = generate_sensor_data()
    print(json.dumps(sensor_data, indent=2, ensure_ascii=False))

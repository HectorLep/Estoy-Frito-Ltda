# Estoy Frito Ltda - Dashboard Ambiental

**Proyecto #3 INFO1128**

Este sistema monitorea sensores ambientales y envía datos en tiempo real usando Python, Node-RED, Grafana, y MQTT (Mosquitto).

---

## ¿Qué hacer primero?

### 1. Instala dependencias de Python
```bash
pip install -r requirements.txt
```

### 2. Configura Mosquitto Broker
Configura los usuarios del broker:
```bash
sudo mosquitto_passwd -c /etc/mosquitto/passwd publisher
# Password: pub123
sudo mosquitto_passwd /etc/mosquitto/passwd subscriber
# Password: sub123
sudo cp mosquitto_config.conf /etc/mosquitto/conf.d/
sudo systemctl restart mosquitto
```

### 3. Inicia Node-RED
```bash
node-red
```
Luego en http://localhost:1880 crea estos endpoints:
- `/sensor_data` para HTTP POST desde Python
- `/sensor_data_mqtt` para datos reenviados por MQTT
Configura nodos de dashboard para visualizar temperatura, humedad, IAQ.

### 4. Inicia Grafana
```bash
sudo systemctl start grafana-server
```
Accede a http://localhost:3000 y configura el datasource (puedes usar JSON API, SimpleJSON o InfluxDB).

### 5. Prueba los scripts Python
Abre terminales y corre:
```bash
python3 generate_json.py          # Solo muestra datos
python3 http_post_nodered.py      # Envía a Node-RED por HTTP
python3 http_post_grafana.py      # Envía a Grafana por HTTP
python3 mqtt_publisher.py         # Publica en MQTT
python3 mqtt_subscriber.py        # Recibe MQTT y reenvía a Node-RED
```

---

## Flujos básicos Node-RED
- Flow HTTP: `[http in: /sensor_data] → [json] → [function] → [dashboard nodes]`
- Flow MQTT: `[http in: /sensor_data_mqtt] → [json] → [function] → [dashboard nodes]`

---

## Commit inicial
Este commit incluye todos los scripts esenciales y configuración básica. Progreso y cambios se documentarán acá.

---

## Contacto
Autor: HectorLep
Para dudas agrega un issue en GitHub.

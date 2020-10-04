#!/usr/bin/python

from json import loads, dumps

import pandas as pd
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("tnt")


def on_message(client, userdata, msg):
    
    payload = loads(msg.payload)

    data = pd.DataFrame([{
        'Tempo': payload['Tempo'],
        'Estação': payload['Estação'],
        'LAT': payload['LAT'],
        'LONG': payload['LONG'],
        'Movimentação': payload['Movimentação'],
        'Original_473': payload['Original_473'],
        'Original_269': payload['Original_269'],
        'Zero': payload['Zero'],
        'Maçã-Verde': payload['Maçã-Verde'],
        'Tangerina': payload['Tangerina'],
        'Citrus': payload['Citrus'],
        'Açaí-Guaraná': payload['Açaí-Guaraná'],
        'Pêssego': payload['Pêssego'],
        'TARGET': payload['TARGET'],
        'row': payload['row']
    }])

    data.to_csv('base_dataset.csv', index=False, header=None, mode='a')

    print(dumps(payload, indent=4, ensure_ascii=False).encode('utf8').decode())


pd.DataFrame(columns=[
    'Tempo', 
    'Estação', 
    'LAT', 
    'LONG', 
    'Movimentação', 
    'Original_473', 
    'Original_269', 
    'Zero', 
    'Maçã-Verde', 
    'Tangerina', 
    'Citrus', 
    'Açaí-Guaraná', 
    'Pêssego', 
    'TARGET',
    'row'
]).to_csv('base_dataset.csv', index=False)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("maratoners", "ndsjknvkdnvjsbvj")

client.connect("tnt-iot.maratona.dev", 30573, 60)

client.loop_forever()

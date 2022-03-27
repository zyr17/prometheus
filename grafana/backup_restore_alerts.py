#!/usr/bin/env python3
import requests
import json
import sys
import os

try:
    USERNAME = os.environ['GRAFANA_USERNAME']
    PASSWORD = os.environ['GRAFANA_PASSWORD']
except:
    print('set env GRAFANA_USERNAME and GRAFANA_PASSWORD')
    exit()

HOSTNAME = 'localhost'
PORT = 3000

request_url = f'http://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}'

rule_url = 'api/ruler/grafana/api/v1/rules'
folder_url='api/folders'
datasource_url = 'api/datasources'

headers = { 'Content-type': 'application/json' }

def mkdir_if_not_exist(folder):
    r = requests.get(f'{request_url}/{folder_url}', headers = headers)
    current = r.json()
    if folder not in [x['title'] for x in current]:
        r = requests.post(
            f'{request_url}/{folder_url}', 
            data = json.dumps({ 'title': folder }),
            headers = headers
        )
        print(f'make folder {folder}')
        if r.status_code // 100 != 2:
            print('{r.status_code} {r.text}')

def get_datasources():
    r = requests.get(f'{request_url}/{datasource_url}', headers = headers)
    if r.status_code // 100 != 2:
        print(r.status_code, r.json())
    r = r.json()
    if len(r) != 1:
        print('datasource length is not 1! currently not supported')
        exit()
    return r[0]['uid']

def get_alerts():
    r = requests.get(f'{request_url}/{rule_url}', headers = headers)
    if r.status_code // 100 != 2:
        print(r.status_code, r.json())
    return json.dumps(r.json(), indent = 2)

def add_one_alert(folder, alert):
    ds = get_datasources()
    for rule in alert['rules']:
        if 'grafana_alert' in rule:
            # remove uid. otherwise api will replace existed rule, and if uid not exist, will raise 400 error
            del rule['grafana_alert']['uid']
            for d in rule['grafana_alert']['data']:
                if len(d['datasourceUid']) == 17:  # datasource is from database, not self
                    d['datasourceUid'] = ds
    r = requests.post(
        f'{request_url}/{rule_url}/{folder}', 
        data = json.dumps(alert),
        headers = headers)
    print(f'add rule {alert["name"]} {r.status_code} {r.text}')

def add_alerts(data):
    for folder in data:
        mkdir_if_not_exist(folder)
        for alert in data[folder]:
            add_one_alert(folder, alert)

if len(sys.argv) < 2 or sys.argv[1] not in ['backup', 'restore']:
    print(f'usage: backup_restore_alert.py  backup/restore  [filename]')
    exit()

filename = 'alerts.json'
if len(sys.argv) > 2:
    filename = sys.argv[2]

if sys.argv[1] == 'backup':
    open(filename, 'w').write(get_alerts())
elif sys.argv[1] == 'restore':
    add_alerts(json.load(open(filename)))

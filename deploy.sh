#!/bin/bash

HOSTNAME=$(hostname) docker stack deploy -c docker-stack.yml prom
python3 prometheus_text_metric_scripts/sync_scripts.py

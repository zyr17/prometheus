#!/usr/bin/env python3

import os
import re

def hosts_file_filter(lines):
    return [x.strip() for x in lines if x.strip() != '' and x.strip()[0] != '#'] 

now_dns = hosts_file_filter(open('/etc/hosts').readlines())

localhost = 'node26'

folderpath = os.path.abspath(os.path.dirname(__file__))
foldername = folderpath.split('/')[-1]

def valid_dns(dns):
    try:
        # print(re.sub(r'[ \t]+', ' ', dns).split(' '))
        ip, hostname = re.sub(r'[ \t]+', ' ', dns).split(' ')
        if ip[:3] != '127' and ':' not in ip and sum([x == hostname[:len(x)] for x in ['node', 'idc']]) > 0:
            # not start with 127; not ipv6; hostname start with keyword
            return True, ip, hostname
    except:
        pass
    return False, None, None

def sync_hosts(sync_lines, ip, target):
    print(f'----- {ip} {target} -----')
    target_hosts = hosts_file_filter(os.popen(f'ssh {ip} -p 30022 cat /etc/hosts').readlines())
    result_lines = []
    for dns in target_hosts:
        if not valid_dns(dns)[0]:
            result_lines.append(dns)  # keep not valid, filter valid, and append later
    for ip, hostname in sync_lines:
        result_lines.append(f'{ip}\t{hostname}')
    print('\n'.join(result_lines))
    tmpfile = '/tmp/hosts'
    open(tmpfile, 'w').write('\n'.join(result_lines))
    os.system(f'ssh {target} -p 30022 cp /etc/hosts /etc/hosts.bak')
    os.system(f'scp -P 30022 /tmp/hosts {target}:/etc/hosts')

sync_lines = []

for dns in now_dns:
    # print(dns)
    res = valid_dns(dns)
    if res[0]:
        sync_lines.append(res[1:])

print(sync_lines)
print(folderpath, foldername)

for ip, hostname in sync_lines:
    print(ip)
    os.system(f'rsync -azr "{folderpath}" {hostname}:~/')
    os.system(f'ssh {hostname} rm /etc/cron.d/prometheus_text_metrics_cron')
    os.system(f'ssh {hostname} ln -s "/root/{foldername}/prometheus_text_metrics_cron" /etc/cron.d/')

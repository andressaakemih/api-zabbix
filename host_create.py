from zabbix_api import ZabbixAPI
import csv
import time

URL = 'http://URL/'
USERNAME = 'user'
PASSWORD = 'pass'

try:
    zapi = ZabbixAPI(URL, timeout=15)
    zapi.login(USERNAME, PASSWORD)
    print(zapi.api_version())
    print(f'Conectado na API do Zabbix, versão atual {zapi.api_version()}')
except Exception as err:
    print(f'Falha ao conectar na API do Zabbix, erro: {err}')
    
info_interfaces = {
    "1": {"type": "agent", "id": "1", "port": "10050"},
    "2": {"type": "SNMP", "id": "2", "port": "161"}    
}

groupids = ['52']
groups = [{"groupid": groupid} for groupid in groupids]

def create_host(host, ip, site_city, location, site_zip, location_lat, location_lon, contact, contract_number):       
    try:
        create_host = zapi.host.create({
            "groups": groups,
            "host": host,
            "interfaces": {
                "type": info_interfaces['1']['id'],
                "main": 1,
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": info_interfaces['1']['port']
            },            
            "inventory_mode": 0,         
            "inventory": {
                "site_city": site_city,
                "location": location,
                "site_zip": site_zip,
                "location_lat": location_lat,
                "location_lon": location_lon,
                "contact": contact,
                "contract_number": contract_number                
            }
        })
        print(f'Host cadastrado com sucesso {host}')
    except Exception as err:
        print(f'Falha ou cadastrar o host: erro {err}')

start_time = time.time()
with open('hosts.csv', encoding='UTF-8') as file:
    file_csv = csv.reader(file, delimiter=';')
    for [hostname,ipaddress,site_city,location,site_zip,location_lat,location_lon,contact,contract_number] in file_csv:
        create_host(hostname,ipaddress,site_city,location,site_zip,location_lat,location_lon,contact,contract_number) 
time.sleep(1)
end_time = time.time()
total_time = (end_time-start_time)*1000
print(f'Total time = {total_time:.2f} ms')
## Zabbix API

Documentação: https://www.zabbix.com/documentation/6.0/en/manual/api
Vídeo: https://www.youtube.com/watch?v=geCC8TupE8w&t=2280s

## Passos:

1. Alterar a URL para o DNS do Zabbix que deseja inserir os hosts

```python
URL = 'https://localhost/'
```

1. Alterar o token
    1. Menu
        1. User settings > Tokens da API
        2. Gerar um

```python
zapi.auth = 'token'
```

1. Colocar o ID do grupo dos hosts que deseja inserir
    1. Menu
        1. Configurações > Grupos de Hosts > Grupo > Nº final da URL

```python
groupids = ['65', '20', '61']
```

1. Passando os dados que precisa inserir do Host

```python
create_host(**host, ip, site_city**)
```

1. Dados do host
    1. groups, host, interfaces (type, ip, dns, port), tamplate, proxy, inventory (site_city)

1. Abre o arquivo CSV (precisa estar com o nome **host.csv**), neste arquivo deve estar em ordem conforme infomado, por ex:

```python
for [hostname,ip,site_city] in file_csv    
```

**Arquivo hosts.csv:**

Host 1; 111.111.11.11; Cuiaba

Host 2; 111.111.11.11; Cuiaba

Arquivo completo:

```python
from zabbix_api import ZabbixAPI
import csv
import time

URL = 'https://localhost/'
# USERNAME = 'user'
# PASSWORD = 'pass'

try:
    zapi = ZabbixAPI(URL, timeout=15)
		# token gerado pelo Zabbix: User settings > Tokens da API
    zapi.auth = 'token gerado pelo zabbix'
    zapi.validate_certs = True
		# zapi.login(USERNAME, PASSWORD)
    print(zapi.api_version())
    print(f'Conectado na API do Zabbix, versão atual {zapi.api_version()}')
except Exception as err:
    print(f'Falha ao conectar na API do Zabbix, erro: {err}')
    
info_interfaces = {
    "1": {"type": "agent", "id": "1", "port": "10050"},
    "2": {"type": "SNMP", "id": "2", "port": "161"}    
}

# colocar os IDs dos grupos dos Hosts
groupids = ['65', '20', '61']
groups = [{"groupid": groupid} for groupid in groupids]

def create_host(host, ip, site_city):       
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
            "templates": {
                "templateid": "10186"
            },
            "proxy_hostid": "11501",
            "inventory_mode": 0,         
            "inventory": {
                "site_city": site_city             
            }
        })
        print(f'Host cadastrado com sucesso {host}')
    except Exception as err:
        print(f'Falha ou cadastrar o host: erro {err}')

start_time = time.time()
with open('hosts.csv', encoding='utf-8') as file:
    file_csv = csv.reader(file, delimiter=';')
    for [hostname,ip,site_city] in file_csv:
        create_host(hostname,ip,site_city) 
time.sleep(1)
end_time = time.time()
total_time = (end_time-start_time)*1000
print(f'Total time = {total_time:.2f} ms')
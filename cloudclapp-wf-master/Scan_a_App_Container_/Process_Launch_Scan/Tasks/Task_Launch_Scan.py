import requests
import json
import time
from pathlib import Path
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import util

dev_var = Variables()
dev_var.add('is_private_registry', var_type='Boolean')
dev_var.add('registry_username', var_type='Composite')
dev_var.add('registry_password', var_type='Composite')
dev_var.add('total_vulnerabilities', var_type='Integer')
dev_var.add('containers.0.name', var_type='String')


context = Variables.task_call(dev_var)
ubiqubeId = context['UBIQUBEID']
snyk_token = '11eee98f-b9e4-41d8-a28d-b8696e9179d8'
def launch_scan(context, container_name):
    payload = '{ "account": { "token": "SNYK_TOKEN" REGISTRY_CREDENTIALS }, "containerName": "CONTAINER_NAME"}'
    registry_credentials = ', "registryUsername": "REGISTRY_USERNAME", "registryPassword": "REGISTRY_PASSWORD"'
    payload = payload.replace('SNYK_TOKEN', snyk_token)
    if context['is_private_registry'] is True:
        registry_credentials = registry_credentials.replace('REGISTRY_USERNAME', context['registry_username'])
        registry_credentials = registry_credentials.replace('REGISTRY_PASSWORD', context['registry_password'])
        payload = payload.replace('REGISTRY_CREDENTIALS', registry_credentials)
    else:
        payload = payload.replace('REGISTRY_CREDENTIALS', "")
    payload = payload.replace('CONTAINER_NAME', container_name)
    post_url = 'http://ccla-scan-app:8080/snyk/scan/container'
    post_headers = { "accept" : "*/*", "Content-Type" : "application/json" }
    post_response = requests.post(post_url, data=payload, headers=post_headers)
    result = post_response.headers
    get_url = result['Location']
    return get_url
    
def get_scan_status(get_url):
    get_headers = { "accept" : "application/hal+json" }
    get_response = requests.get(get_url, headers=get_headers)
    return json.loads(get_response.content)

containers = context.get('containers')

scan_map = {}
for container in containers:
  get_url = launch_scan(context, container['name'])
  scan_map[container['name']] = get_url
  
ret = ""
total_vulnerabilities = 0
scan_failed = False
while scan_map:
	for container_name, get_url in list(scan_map.items()):
		scan_status = get_scan_status(get_url)
		status = scan_status['runStatus']
		index = containers.index(next(filter(lambda n: n.get('name') == container_name, containers)))
		util.log_to_process_file(context['SERVICEINSTANCEID'], "SCAN_STATUS:  "+container_name+" : "+status+"\n", context['PROCESSINSTANCEID'])
		if status == 'RUNNING' or status == 'NOT_STARTED':
			time.sleep(5)
		elif status == 'SUCCESS':
			del scan_map[container_name]
			vulnerabilities = scan_status['vulnerabilities']
			if len(vulnerabilities) == 0:
				context['containers'][index]['vulnerabilities_json_file'] = 'No Vulnerabilities Found'
				context['containers'][index]['vulnerabilities'] = 0
			else:
				json_object = json.dumps(scan_status, indent = 4)
				path = Path('/opt/fmc_repository/Datafiles/ccla_scan_app/'+ubiqubeId+'/'+context['SERVICEINSTANCEID'])
				path.mkdir(parents=True, exist_ok=True)
				container_name_json = container_name.replace("/","_")
				vulnerabilities_json_file = str(path)+"/vulnerabilities_"+container_name_json+".json"
				with open(vulnerabilities_json_file, "w") as outfile:
					outfile.write(json_object)
				context['containers'][index]['vulnerabilities_json_file'] = vulnerabilities_json_file
				context['containers'][index]['vulnerabilities'] = len(vulnerabilities)
				total_vulnerabilities = total_vulnerabilities + len(vulnerabilities)
				context['containers'][index]['scan_status'] = 'SUCCESS'
							
				json_data = json.loads(json_object)
				low_count = 0
				info_count = 0
				medium_count = 0
				high_count = 0
				critical_count=0
					
				vulns = json_data['vulnerabilities']
				for item in vulns:
					risk_type = item['severity']
					if risk_type.lower() == "low":
						low_count += 1
					elif risk_type.lower() == "informational":
						info_count +=1
					elif risk_type.lower() == "medium":
						medium_count +=1
					elif risk_type.lower() == "high":
						high_count +=1
					elif risk_type.lower() == "critical":
						critical_count +=1
					else:
						continue 
				
				context['containers'][index]['info_count'] = info_count
				context['containers'][index]['low_count'] = low_count
				context['containers'][index]['medium_count'] = medium_count
				context['containers'][index]['high_count'] = high_count
				context['containers'][index]['critical_count'] = critical_count
				
		else:
			scan_failed = True
			del scan_map[container_name]
			error = scan_status['error']['detail']
			context['containers'][index]['scan_status'] = 'FAILED, Error:'+error

context['total_vulnerabilities'] = total_vulnerabilities			
if scan_failed:
	ret = MSA_API.process_content('FAILED', error, context, True)
else:
	ret = MSA_API.process_content('ENDED', 'Scan Complete', context, True)
print(ret)

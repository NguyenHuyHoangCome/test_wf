import requests
import json
import time
from pathlib import Path
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import util
from zapv2 import ZAPv2

dev_var = Variables()
context = Variables.task_call(dev_var)
ubiqubeId = context['UBIQUBEID']
apikey = '7da091fe-63a4-48c0-9bfa-7614c49feb7c'
zap = ZAPv2(apikey=apikey, proxies={'http': 'http://ccla-scan-env:8080', 'https': 'https://ccla-scan-env:8080'})

def launch_spider_scan(target):
    zap.urlopen(target)
    time.sleep(3)
    scan_id = zap.spider.scan(target)
    return scan_id
    
def launch_active_scan(target):
    scan_id = zap.ascan.scan(target)
    return scan_id

def get_scan_report(target):
	result = zap.core.alerts(target)
	return result

scan_id = launch_spider_scan(context['target'])
scan_complete_precentage = int(zap.spider.status(scan_id))
while int(zap.spider.status(scan_id)) < 100:
	time.sleep(3)
	scan_complete_precentage = int(zap.spider.status(scan_id))


#scan_id = launch_active_scan(context['target'])
#scan_complete_precentage = int(zap.ascan.status(scan_id))
#while int(zap.ascan.status(scan_id)) < 100:
#	time.sleep(3)
#	scan_complete_precentage = int(zap.ascan.status(scan_id))

if scan_complete_precentage == 100:
	alerts = get_scan_report(context['target'])
	json_object = json.dumps(alerts, indent = 4)
	path = Path('/opt/fmc_repository/Datafiles/ccla_scan_webapp/'+ubiqubeId+'/'+context['SERVICEINSTANCEID'])
	path.mkdir(parents=True, exist_ok=True)
	alerts_json_file = str(path)+"/alerts.json"
	with open(alerts_json_file, "w") as outfile:
		outfile.write(json_object)
	context['alerts_json_file'] = alerts_json_file
	context['total_alerts'] = len(alerts)
	
	json_data = json.loads(json_object)
	low_count = 0
	info_count = 0
	medium_count = 0
	high_count = 0
	
	for item in json_data:
		risk_type = item['risk']
		if risk_type.lower() == "low":
			low_count += 1
		elif risk_type.lower() == "informational":
			info_count +=1
		elif risk_type.lower() == "medium":
			medium_count +=1
		elif risk_type.lower() == "high":
			high_count +=1
		else:
			continue 

	context['info_count'] = info_count
	context['low_count'] = low_count
	context['medium_count'] = medium_count
	context['high_count'] = high_count
	
	ret = MSA_API.process_content('ENDED', 'Scan Complete', context, True)
print(ret)

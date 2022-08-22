import subprocess
import os
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.orchestration import Orchestration
from msa_sdk import util

dev_var = Variables()
context = Variables.task_call(dev_var)

def is_pingable(host):
	try:
		subprocess.check_output(["ping", "-c", "1", host])
		return True
	except subprocess.CalledProcessError:
		return False

subtenant_ext_ref = context['UBIQUBEID']
Orchestration = Orchestration(subtenant_ext_ref)
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

if __name__ == "__main__":
	Orchestration.update_asynchronous_task_details(*async_update_list, f'ping GKE host')
	host = context.get('cluster_ip');
	if is_pingable(host):
		cluster_status = 'ACTIVE'
	else:
		cluster_status = 'INACTIVE'
	context.update(cluster_status=cluster_status)

ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)


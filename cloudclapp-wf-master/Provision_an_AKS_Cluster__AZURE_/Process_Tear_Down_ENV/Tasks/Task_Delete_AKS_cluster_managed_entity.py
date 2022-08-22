import subprocess
import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration
from msa_sdk.device import Device

dev_var = Variables()
context = Variables.task_call(dev_var)

subtenant_ext_ref = context['UBIQUBEID']
Orchestration = Orchestration(subtenant_ext_ref)
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

if not context.get('is_cluster_created'):
	    MSA_API.task_success('No ME to delete', context)
	    sys.exit()

if __name__ == "__main__":
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Delete Managed Entity ...')
    #get device id.
    device_ref = context.get('aks_cluster_me_ext_ref')
    device_id = device_ref[3:]
    #initialize Device object based-on the device id.
    device = Device(device_id=device_id)
    #remove managed entity.
    device.delete(device_ref)
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Delete Managed Entity ...OK')
    
    MSA_API.task_success('The AKS cluster managed entity with ' + 'id=' + device_id + ' is deleted.', context)
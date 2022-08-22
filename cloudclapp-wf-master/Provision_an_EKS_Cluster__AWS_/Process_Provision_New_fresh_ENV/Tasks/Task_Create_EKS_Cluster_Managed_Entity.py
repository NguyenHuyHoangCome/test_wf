import subprocess
import json
import re
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration
from msa_sdk.device import Device
from msa_sdk import util

dev_var = Variables()
context = Variables.task_call(dev_var)

'''
Allows execution of terraform locaaly.
'''
def terraform_run(command, Orchestration):
    output = ''
    ret = ''
    process = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True)
    while True:
        output = process.stdout.readline()
        util.log_to_process_file(context['SERVICEINSTANCEID'], output, context['PROCESSINSTANCEID'])
        # Do something else
        return_code = process.poll()
        if return_code is not None:
            # Process has finished, read rest of the output 
            for ret in process.stdout.readline():
                try:
                    util.log_to_process_file(context['SERVICEINSTANCEID'], ret.strip(), context['PROCESSINSTANCEID'])
                except TypeError:
                    continue
            break
        #else:
            #MSA_API.task_error('The TF init is failed: ' + ret , context)
    return output + ret

'''
allows to get terraform output resource value.
'''
def get_tf_output_value(tf_workspace, resource_name, Orchestration):
    #Prepare command as list.
    tf_chdir = '-chdir=' + tf_workspace
    command = ['terraform',tf_chdir,'output','-raw', resource_name]
    #execute command.
    ret = terraform_run(command, Orchestration)
    return ret

def get_cluster_ip(cluster_endpoint):
	cluster_endpoint = cluster_endpoint.replace("https://", "")
	result = subprocess.run(['ping', '-c', '1', cluster_endpoint], stdout=subprocess.PIPE)
	input = str(result.stdout)
	cluster_endpoint = cluster_endpoint.replace(".", "\.")
	output = re.search('PING\s'+cluster_endpoint+'\s\((\S+)\)\s', input, flags=re.IGNORECASE)
	if output is not None:
		cluster_ip = output.group(1)
		return cluster_ip
	else:
		MSA_API.task_error('Failed Fetch Cluster Ip ', context)

subtenant_ext_ref = context['UBIQUBEID']
Orchestration = Orchestration(subtenant_ext_ref)
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

if __name__ == "__main__":
    #Message
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Retrieve TF outputs parameters ...')
    #Tf work directory definition
    work_directory = context.get('terraform_provision_eks_cluster_workspace')
    
    ### Get K8s cluster_id
    cluster_id = get_tf_output_value(work_directory, 'cluster_id', Orchestration)
    context.update(cluster_id=cluster_id)
    ### Get K8s cluster_endpoint
    cluster_endpoint = get_tf_output_value(work_directory, 'cluster_endpoint', Orchestration)
    context.update(cluster_endpoint=cluster_endpoint)
    ### Get K8s cluster_name
    cluster_name = get_tf_output_value(work_directory, 'cluster_name', Orchestration)
    context.update(cluster_name=cluster_name)
    ### Get K8s cluster cluster_ca_certificate
    cluster_ca_certificate = get_tf_output_value(work_directory, 'cluster_ca_certificate', Orchestration)
    context.update(cluster_ca_certificate=cluster_ca_certificate)
    ### Get K8s cluster region
    region = get_tf_output_value(work_directory, 'region', Orchestration)
    context.update(region=region)
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Retrieve TF output parameters ...OK')
    #Initiate Device object
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Create Managed Entity ...')
    #Customer ID
    customer_id = subtenant_ext_ref[4:]
    #Kubernetes_generic manufacturer_id
    manufacturer_id='20060101'
    #Kubernetes_generic model_id
    model_id='20060101'
    #default IP address
    management_address= get_cluster_ip(cluster_endpoint)
    #Kubernetes adaptor does not use the password and login of ME.
    password = 'fake38passwOrd'
    management_port='443'
    #Create Device
    device = Device(customer_id=customer_id, name=cluster_name, manufacturer_id=manufacturer_id, model_id=model_id, login=cluster_name, password=cluster_id, password_admin=cluster_id, management_address=management_address, management_port=management_port, device_external="", log_enabled=False, log_more_enabled=False, mail_alerting=False, reporting=False, snmp_community='ubiqube', device_id="")
    response = device.create()
    device.activate()
    context.update(device=response)
    #get device external reference
    device_ext_ref = response.get('externalReference')
    context.update(eks_cluster_me_ext_ref=device_ext_ref)
    
    #get device external reference
    device_id = response.get('id')
    context.update(eks_cluster_me_id=device_id)
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Create Managed Entity ...OK')
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Store TF output parameters to Managed Entity ...OK')
    
    device.create_configuration_variable('cluster_tf_chdir', work_directory)
    device.create_configuration_variable('cluster_endpoint', cluster_endpoint)
    device.create_configuration_variable('cluster_name', cluster_name)
    device.create_configuration_variable('cluster_ca_certificate', cluster_ca_certificate)
    device.create_configuration_variable('region', region)
    device.create_configuration_variable('cluster_id', cluster_id)
    
    MSA_API.task_success('The EKS cluster managed entity is created with external Id: ' + device_ext_ref, context)
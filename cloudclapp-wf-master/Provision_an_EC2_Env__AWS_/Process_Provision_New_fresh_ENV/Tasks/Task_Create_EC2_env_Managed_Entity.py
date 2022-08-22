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
    result = ''
    process = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True)
    while True:
        output += process.stdout.readline()
        util.log_to_process_file(context['SERVICEINSTANCEID'], "OUTPUTsss:"+output, context['PROCESSINSTANCEID'])
        # Do something else
        return_code = process.poll()
        if return_code is not None:
            # Process has finished, read rest of the output 
            for ret in process.stdout.readline():
                try:
                    result += ret
                    util.log_to_process_file(context['SERVICEINSTANCEID'], ret.strip(), context['PROCESSINSTANCEID'])
                except TypeError:
                    continue
            break
        #else:
            #MSA_API.task_error('The TF init is failed: ' + ret , context)
    return output + result

'''
allows to get terraform output resource value.
'''
def get_tf_output_value(tf_workspace, resource_name, Orchestration, o_type='-raw'):
    #Prepare command as list.
    tf_chdir = '-chdir=' + tf_workspace
    command = ['terraform',tf_chdir,'output',o_type, resource_name]
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
    work_directory = context.get('terraform_provision_ec2_vpc_workspace')
    
    ### Get VPC ID
    vpc_id = get_tf_output_value(work_directory, 'vpc_id', Orchestration)
    context.update(vpc_id=vpc_id)
    
    ### Get VPC Name
    vpc_name = get_tf_output_value(work_directory, 'vpc_name', Orchestration)
    context.update(vpc_name=vpc_name)
    
    security_group_id = get_tf_output_value(work_directory, 'security_group_id', Orchestration)
    context.update(security_group_id=security_group_id)
    
    ### Get Private subnets
    private_subnets = get_tf_output_value(work_directory, 'private_subnets', Orchestration, '-json')
    util.log_to_process_file(context['SERVICEINSTANCEID'], "private_subnets:"+private_subnets, context['PROCESSINSTANCEID'])
    private_subnet_list = json.loads(private_subnets)
    private_subnet=private_subnet_list[0]
    context.update(private_subnet=private_subnet)
    
    ### Get Public subnets
    public_subnets = get_tf_output_value(work_directory, 'public_subnets', Orchestration, '-json')
    public_subnet_list = json.loads(public_subnets)
    public_subnet=public_subnet_list[0]
    context.update(public_subnet=public_subnet)
    
    ### Get security group id
    
    
    #### Get region
    region = get_tf_output_value(work_directory, 'region', Orchestration)
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Retrieve TF output parameters ...OK')
    #Initiate Device object
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Create Managed Entity ...')
    #Customer ID
    customer_id = subtenant_ext_ref[4:]
    #AWS_generic manufacturer_id
    manufacturer_id='17010301'
    #AWS_generic model_id
    model_id='17010301'
    #default IP address
    management_address= '1.1.1.1'
    #Kubernetes adaptor does not use the password and login of ME.
    password = 'fake38passwOrd'
    management_port='443'
    
    name = vpc_name
    
    #Check if a ME is already created.
    if not context.get('ec2_vpc_me_ext_ref'):
        #Create Device
        device = Device(customer_id=customer_id, name=name, manufacturer_id=manufacturer_id, model_id=model_id, login=vpc_id, password=vpc_id, password_admin=vpc_id, management_address=management_address, management_port=management_port, device_external="", log_enabled=False, log_more_enabled=False, mail_alerting=False, reporting=False, snmp_community='ubiqube', device_id="")
        response = device.create()
        device.activate()
        context.update(device=response)
        #get device external reference
        device_ext_ref = response.get('externalReference')
        context.update(ec2_vpc_me_ext_ref=device_ext_ref)
        
        #get device external reference
        device_id = response.get('id')
        context.update(ec2_vpc_me_id=device_id)
        
        Orchestration.update_asynchronous_task_details(*async_update_list, f'Create Managed Entity ...OK')
        
        Orchestration.update_asynchronous_task_details(*async_update_list, f'Store TF output parameters to Managed Entity ...OK')
        
        device.create_configuration_variable('ec2_tf_chdir', work_directory)
        device.create_configuration_variable('ec2_vpc_id', vpc_id)
        device.create_configuration_variable('ec2_region', region)
        device.create_configuration_variable('private_subnet', private_subnet)
        device.create_configuration_variable('public_subnet', public_subnet)
        device.create_configuration_variable('ec2_vpc_name', vpc_name)
        device.create_configuration_variable('ec2_vpc_security_group_id', security_group_id)
    
    MSA_API.task_success('The EC2 managed entity is created with external Id: ' + device_ext_ref, context)
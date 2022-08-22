import json
import subprocess
import os
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.orchestration import Orchestration
from msa_sdk.device import Device

dev_var = Variables()
context = Variables.task_call(dev_var)


'''
allows to get configuration variable value.
'''
def _get_configuration_variable(device, name):
    value = ''
    ret = device.get_configuration_variable(name)
    if 'value' in ret:
        value = ret.get('value')
        return value
    return ''

'''
Allows to merge dictionnaries in list as one dictionnary.
'''
def _merge_dicts_as_one_super_dict(dict_list):
    super_dict = {}
    for d in dict_list:
        key = ''
        value = ''
        for k, v in d.items():
            if k == 'key':
                key = "CLOUDCLAPP_"+v
            elif k == 'value':
                value = v
        super_dict.setdefault(key, value)
            
    return super_dict
    
#Variables.
subtenant_ext_ref = context['UBIQUBEID']
Orchestration = Orchestration(subtenant_ext_ref)
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

if __name__ == "__main__":
    
    #Retrieve AWS EC2 Env. authentification informations from infrastructure Managed Entity configuration variables.
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Retrieve AWS authentification details ...')
    #Get AWS EC2 Env. ME external reference.
    device_ext_ref = context.get('env_infrastructure_me')
    if not device_ext_ref:
        MSA_API.task_error('The AWS EC2 Env. Managed Entity is missing from input variables.', context)
    
    #Intialize Device from device ID:
    device_id = device_ext_ref[3:]
    device = Device(device_id=device_id)
    
    #get work_directory from device configuration config
    vpc_tf_work_directory = _get_configuration_variable(device, 'ec2_tf_chdir')
    
    vpc_tf_tfvar_file = vpc_tf_work_directory +"/terraform.tfvars"
    
    aws_credentials = subprocess.getoutput("grep -E 'access_key|secret_key|region' "+vpc_tf_tfvar_file)
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Retrieve Retrieve AWS  authentification details ...OK')
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Retrieve EC2 VPC Id ...')
    #Get configuration variables from infrastructure ME.
    ec2_vpc_id = _get_configuration_variable(device, 'ec2_vpc_id')
    ec2_vpc_security_group_id = _get_configuration_variable(device, 'ec2_vpc_security_group_id')
    ec2_vpc_private_subnet = _get_configuration_variable(device, 'private_subnet')
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Retrieve EC2 VPC Id ...OK')
    
    #Terraform work directory.
    workspace_dir = context.get('terraform_provision_app_workspace')
    #terraform variables file.
    tfvars_file = workspace_dir + "/terraform.tfvars"
    #EC2 Resources tags.
    tags = context.get('tags')
    if tags is not None:
        all_tags = _merge_dicts_as_one_super_dict(tags)
    else:
    	all_tags = dict()
    #Set terraform variables values in terraform.tfstate file.
    with open(tfvars_file) as f:
        newText = f.read().replace('additional_tags_value', json.dumps(all_tags))
        newText = newText.replace('vpc_id_value', ec2_vpc_id)
        newText = newText.replace('security_group_id_value', ec2_vpc_security_group_id)
        newText = newText.replace('vpc_subnet_id_value', ec2_vpc_private_subnet)
        newText += aws_credentials+"\n"
        
    with open(tfvars_file, "w") as f:
        f.write(newText)
    
    tfvars_template_file = workspace_dir + "/ec2_instance_tfvar_template"
    ec2_instance_template_file = workspace_dir + "/ec2_instance_template"
    ec2_instances_file = workspace_dir + "/ec2_instances.tf"
    
    ec2_instances = context.get('apps_to_deploy')
    
    
    
    i = 0
    for ec2_instance in ec2_instances:
        with open(ec2_instance_template_file) as f:
            ec2_instance_content = f.read().replace('instance_no', str(i))
        with open(ec2_instances_file, "a") as f: 
            f.write(ec2_instance_content)
            f.write('\n')
        with open(tfvars_template_file) as f:
            ec2_instance_tfvars_content = f.read().replace('instance_no', str(i))
            ec2_instance_tfvars_content = ec2_instance_tfvars_content.replace('ec2_instances.'+str(i)+'.aws_ami_id_value', ec2_instance['aws_ami_id'])
            ec2_instance_tfvars_content = ec2_instance_tfvars_content.replace('ec2_instances.'+str(i)+'.aws_instance_type_value', ec2_instance['aws_instance_type'])
            ec2_instance_tfvars_content = ec2_instance_tfvars_content.replace('ec2_instances.'+str(i)+'.aws_instance_name_value', ec2_instance['aws_instance_name'])
        with open(tfvars_file, "a") as f:
            f.write(ec2_instance_tfvars_content)
            f.write('\n')
        i += 1
    os.remove(tfvars_template_file)
    os.remove(ec2_instance_template_file)
    ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
    print(ret)


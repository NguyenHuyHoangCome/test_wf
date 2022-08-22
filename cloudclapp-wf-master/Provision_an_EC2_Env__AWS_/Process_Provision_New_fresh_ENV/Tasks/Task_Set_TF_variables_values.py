import re
import requests
import json
from os import fdopen
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration
from msa_sdk import util

dev_var = Variables()
dev_var.add('aws_region', var_type='String')
dev_var.add('aws_access_key_id', var_type='String')
dev_var.add('aws_secret_access_key', var_type='String')
dev_var.add('use_org_cloud_credentials', var_type='Boolean')
dev_var.add('tags.0.key', var_type='String')
dev_var.add('tags.0.value', var_type='String')
context = Variables.task_call(dev_var)


'''
Set terraform configuration variable value.
'''
def set_tfconfig_variable_value(ftvars_filename, var_name, var_value, context):
    try:
        with open(ftvars_filename, 'r+') as f:
            text = f.read()
            text = re.sub(var_name + "\s+=.*", var_name + " = \"" + var_value + "\"", text)
            f.seek(0)
            f.write(text)
            f.truncate()
            
    except FileNotFoundError:
        MSA_API.task_error('The TFVARS file is not found here: ' + ftvars_filename, context)
    except:
        MSA_API.task_error('Failed to read the TFVARS file: ' + ftvars_filename, context)

'''
Replace line from file.
'''
def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    #Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

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


if bool(context['use_org_cloud_credentials']):
    prefix = subtenant_ext_ref[0:3]
    url = 'http://localhost:8480/ubi-api-rest/ccla/cloud/connections/'+prefix+'/aws/aws-connection-1'
    headers = {"Authorization": "Bearer "+context['TOKEN']}
    response = requests.request('GET', url=url, headers=headers)
    if response.status_code == 200:
        output = json.loads(response.content)
        context['aws_access_key_id'] = output['aws_access_key']
        context['aws_secret_access_key'] = output['aws_secret_key']
    else:
        MSA_API.task_error('No Organisation Credentails Defined ', context)


#Terraform file where the inputs variables will be field in therraform workspace.
TERRAFORM_TFVARS_FILENAME = "terraform.tfvars"
#AWS authentification is based-on "SERVICE authentification" mode.
TERRAFORM_REGION_VAR_NAME = 'region'
TERRAFORM_ID_VAR_NAME = 'access_key'
TERRAFORM_KEY_VAR_NAME = 'secret_key'

if __name__ == "__main__":
    #Message
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Set provider login informations ...')
    
    #Provision AKS cluster terraform configuration filename.
    terraform_provision_ec2_vpc_workspace = context.get('terraform_provision_ec2_vpc_workspace')
    
    #terraform.tfvars filename.
    ftvars_filename = terraform_provision_ec2_vpc_workspace +"/"+ TERRAFORM_TFVARS_FILENAME
    
    #Get CLIENT_ID from context / infra descriptor.
    aws_access_key_id = ''
    if 'aws_access_key_id' in context:
        aws_access_key_id = context.get('aws_access_key_id')
    #update CLIENT_ID variable
    set_tfconfig_variable_value(ftvars_filename, TERRAFORM_ID_VAR_NAME, aws_access_key_id.strip(), context)
    
    #Get CLIENT_PASSWORD from context / infra descriptor.
    aws_secret_access_key = ''
    if 'aws_secret_access_key' in context:
        aws_secret_access_key = context.get('aws_secret_access_key')
    #update CLIENT_PASSWORD variable.
    set_tfconfig_variable_value(ftvars_filename, TERRAFORM_KEY_VAR_NAME, aws_secret_access_key.strip(), context)
    
    #Get REGION from context / infra descriptor.
    aws_region = ''
    if 'aws_region' in context:
        aws_region = context.get('aws_region')
    #update REGION variable.
    set_tfconfig_variable_value(ftvars_filename, TERRAFORM_REGION_VAR_NAME, aws_region.strip(), context)
    
    #EC2 Resources tags.
    tags = context.get('tags')
    if tags is not None:
        all_tags = _merge_dicts_as_one_super_dict(tags)
    else:
    	all_tags = dict()
        
    with open(ftvars_filename) as f:
        newText=f.read().replace('additional_tags_value', json.dumps(all_tags))
    with open(ftvars_filename, "w") as f:
        f.write(newText)
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Set provider login informations ...OK')
    
    MSA_API.task_success('The terraform variables are updated successfully.', context)
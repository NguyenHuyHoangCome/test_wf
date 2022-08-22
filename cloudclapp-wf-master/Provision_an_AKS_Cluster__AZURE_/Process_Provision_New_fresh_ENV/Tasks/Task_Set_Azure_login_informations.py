import re
import requests
import json
from os import fdopen
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration

dev_var = Variables()
dev_var.add('service_principal_client_id', var_type='String')
dev_var.add('service_principal_client_secret', var_type='String')
dev_var.add('service_principal_subscription_id', var_type='String')
dev_var.add('service_principal_tenant_id', var_type='String')
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
    with open(file_path, 'r+') as f:
        newText=f.read().replace(pattern, subst)
        f.seek(0)
        f.write(newText)
        f.truncate()

#Variables.
subtenant_ext_ref = context['UBIQUBEID']
Orchestration = Orchestration(subtenant_ext_ref)
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

if bool(context['use_org_cloud_credentials']):
    prefix = subtenant_ext_ref[0:3]
    url = 'http://localhost:8480/ubi-api-rest/ccla/cloud/connections/'+prefix+'/azure/azure-connection-1'
    headers = {"Authorization": "Bearer "+context['TOKEN']}
    response = requests.request('GET', url=url, headers=headers)
    if response.status_code == 200:
        output = json.loads(response.content)
        context['service_principal_client_id'] = output['service_principal_client_id']
        context['service_principal_client_secret'] = output['service_principal_client_secret']
        context['service_principal_subscription_id'] = output['service_principal_subscription_id']
        context['service_principal_tenant_id'] = output['service_principal_tenant_id']
    else:
        MSA_API.task_error('No Organisation Credentails Defined ', context)

#Terraform file where the inputs variables will be field in therraform workspace.
TERRAFORM_TFVARS_FILENAME = "terraform.tfvars"


if __name__ == "__main__":
    #Message
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Set provider login informations ...')
    
    #Provision AKS cluster terraform configuration filename.
    terraform_provision_aks_cluster_workspace = context.get('terraform_provision_aks_cluster_workspace')
    
    #terraform.tfvars filename.
    ftvars_filename = terraform_provision_aks_cluster_workspace +"/"+ TERRAFORM_TFVARS_FILENAME
    
     #Get CLIENT_ID from context / infra descriptor.
    service_principal_client_id = ''
    if 'service_principal_client_id' in context:
        service_principal_client_id = context.get('service_principal_client_id')
    #update CLIENT_ID variable
    set_tfconfig_variable_value(ftvars_filename, 'clientId', service_principal_client_id.strip(), context)
    
    #Get CLIENT_PASSWORD from context / infra descriptor.
    service_principal_client_secret = ''
    if 'service_principal_client_secret' in context:
        service_principal_client_secret = context.get('service_principal_client_secret')
    #update CLIENT_PASSWORD variable.
    set_tfconfig_variable_value(ftvars_filename, 'clientSecret', service_principal_client_secret.strip(), context)
    
    #Get SUBSCRIPTION from context / infra descriptor.
    service_principal_subscription_id = ''
    if 'service_principal_subscription_id' in context:
        service_principal_subscription_id = context.get('service_principal_subscription_id')
    #update SUBSCRIPTION variable.
    set_tfconfig_variable_value(ftvars_filename, 'subscriptionId', service_principal_subscription_id.strip(), context)
    
    tags = context.get('tags')
    
    tag_content = "CLOUDCLAPP_ENVID=\"" + subtenant_ext_ref + "\"\n"
    
    if tags is not None:
        for tag in tags:
            tag_content += "CLOUDCLAPP_" + tag['key'] + "=\"" + tag['value'] + "\"\n"
    
    aks_file = terraform_provision_aks_cluster_workspace + "/aks-cluster.tf"
    
    replace(aks_file, "#CLOUDCLAPP_TAGS", tag_content)
    
    #Get TENANT from context / infra descriptor.
    service_principal_tenant_id = ''
    if 'service_principal_tenant_id' in context:
        service_principal_tenant_id = context.get('service_principal_tenant_id')
    #update TENANT variable.
    set_tfconfig_variable_value(ftvars_filename, 'tenantId', service_principal_tenant_id.strip(), context)
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Set provider login informations ...OK')
    
    MSA_API.task_success('The terraform variables are updated successfully.', context)
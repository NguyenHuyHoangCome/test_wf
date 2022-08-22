'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
import requests
import json
import os
import re
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import util

dev_var = Variables()
dev_var.add('gcp_region', var_type='String')
dev_var.add('gke_num_nodes', var_type='Integer')
dev_var.add('gcp_project_id', var_type='String')
dev_var.add('gcp_private_key_id', var_type='Composite')
dev_var.add('gcp_private_key', var_type='Composite')
dev_var.add('gcp_service_account_email', var_type='String')
dev_var.add('gcp_client_id', var_type='String')
dev_var.add('use_org_cloud_credentials', var_type='Boolean')
dev_var.add('create_new_vpc', var_type='Boolean')
dev_var.add('create_new_subnet', var_type='Composite')
dev_var.add('vpc_name', var_type='String')
dev_var.add('subnet_name', var_type='String')
dev_var.add('ip_cidr_range', var_type='String')
dev_var.add('cluster_name', var_type='String')
context = Variables.task_call(dev_var)

subtenant_ext_ref = context['UBIQUBEID']

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
    except Exception as e:
        MSA_API.task_error('Failed to read the TFVARS file: ' + ftvars_filename + e, context)


if bool(context['use_org_cloud_credentials']):
    prefix = subtenant_ext_ref[0:3]
    url = 'http://localhost:8480/ubi-api-rest/ccla/cloud/connections/'+prefix+'/gcp/gcp-connection-1'
    headers = {"Authorization": "Bearer "+context['TOKEN']}
    response = requests.request('GET', url=url, headers=headers)
    if response.status_code == 200:
        output = json.loads(response.content)
        context['gcp_private_key_id'] = output['gcp_private_key_id']
        context['gcp_private_key'] = repr(output['gcp_private_key']).strip("'")
        context['gcp_service_account_email'] = output['gcp_service_account_email']
        context['gcp_client_id'] = output['gcp_client_id']
    else:
        MSA_API.task_error('No Organisation Credentails Defined ', context)

workspace_dir = context.get('terraform_provision_gke_cluster_workspace')

use_existing_vpc = False
if context['create_new_vpc'] == 'true' or context['create_new_vpc'] == True:
	util.log_to_process_file(context['SERVICEINSTANCEID'], "Creating new VPC", context['PROCESSINSTANCEID'])
else:
	use_existing_vpc= True
	gke_file = open(workspace_dir+"/gke.tf", "rt")
	data = gke_file.read()
	data = data.replace('google_compute_network.vpc.name', 'var.vpc_name')
	gke_file.close()
	gke_file = open(workspace_dir+"/gke.tf", "wt")
	gke_file.write(data)
	gke_file.close()
	os.remove(workspace_dir+"/vpc.tf")
	
if context['create_new_subnet'] == 'true' or context['create_new_subnet'] == True:
	util.log_to_process_file(context['SERVICEINSTANCEID'], "Creating new Subnet", context['PROCESSINSTANCEID'])
	if use_existing_vpc:
		subnet_file = open(workspace_dir+"/subnet.tf", "rt")
		data = subnet_file.read()
		data = data.replace('google_compute_network.vpc.name', 'var.vpc_name')
		subnet_file.close()
		subnet_file = open(workspace_dir+"/subnet.tf", "wt")
		subnet_file.write(data)
		subnet_file.close()
else:
	gke_file = open(workspace_dir+"/gke.tf", "rt")
	data = gke_file.read()
	data = data.replace('google_compute_subnetwork.subnet.name', 'var.subnet_name')
	gke_file.close()
	gke_file = open(workspace_dir+"/gke.tf", "wt")
	gke_file.write(data)
	gke_file.close()
	os.remove(workspace_dir+"/subnet.tf")

TERRAFORM_TFVARS_FILENAME = "terraform.tfvars"

terraform_provision_gke_cluster_workspace = context.get('terraform_provision_gke_cluster_workspace')
ftvars_filename = terraform_provision_gke_cluster_workspace +"/"+ TERRAFORM_TFVARS_FILENAME


gcp_region = ''
if 'gcp_region' in context:
    gcp_region = context.get('gcp_region')
set_tfconfig_variable_value(ftvars_filename, 'region', gcp_region.strip(), context)

gke_num_nodes = ''
if 'gke_num_nodes' in context:
    gke_num_nodes = context.get('gke_num_nodes')
set_tfconfig_variable_value(ftvars_filename, 'gke_num_nodes', gke_num_nodes.strip(), context)

gcp_project_id = ''
if 'gcp_project_id' in context:
    gcp_project_id = context.get('gcp_project_id')
set_tfconfig_variable_value(ftvars_filename, 'project_id', gcp_project_id.strip(), context)

vpc_name = ''
if 'vpc_name' in context:
    vpc_name = context.get('vpc_name')
set_tfconfig_variable_value(ftvars_filename, 'vpc_name', vpc_name.strip(), context)

subnet_name = ''
if 'subnet_name' in context:
    subnet_name = context.get('subnet_name')
set_tfconfig_variable_value(ftvars_filename, 'subnet_name', subnet_name.strip(), context)

ip_cidr_range = ''
if 'ip_cidr_range' in context:
    ip_cidr_range = context.get('ip_cidr_range')
set_tfconfig_variable_value(ftvars_filename, 'ip_cidr_range', ip_cidr_range.strip(), context)

cluster_name = ''
if 'cluster_name' in context:
    cluster_name = context.get('cluster_name')
set_tfconfig_variable_value(ftvars_filename, 'cluster_name', cluster_name.strip(), context)

     
ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)


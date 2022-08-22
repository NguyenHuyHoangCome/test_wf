import os
import uuid
import shutil
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration

dev_var = Variables()
dev_var.add('deployment_name', var_type='String')
dev_var.add('deployment_desc', var_type='String')
dev_var.add('env_infrastructure_me', var_type='Device')
dev_var.add('apps_to_deploy.0.app_name', var_type='String')
dev_var.add('apps_to_deploy.0.short_description', var_type='String')
dev_var.add('apps_to_deploy.0.app_image', var_type='String')
dev_var.add('apps_to_deploy.0.app_replicas', var_type='Integer')
dev_var.add('apps_to_deploy.0.app_port', var_type='Integer')
dev_var.add('apps_to_deploy.0.app_node_port', var_type='Integer')
context = Variables.task_call(dev_var)

subtenant_ext_ref = context['UBIQUBEID']
Orchestration = Orchestration(subtenant_ext_ref)
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

#Terraform workspace base directory in Repository datafiles
TF_APPLICATIONS_WORKSPACES_BASE_DIR = '/opt/fmc_repository/Datafiles/CCLA/Terraform/Applications/Workspaces/'
TF_CONF_TEMPLATE = '/opt/fmc_repository/Process/cloudclapp-wf/Terraform_Configuration_Templates/Applications/Catalogs/gcp/terraform_provision_apps_gke_cluster'


#Read 'APPLICATIONS/environments' description:
Orchestration.update_asynchronous_task_details(*async_update_list, 'Retrieve terraform configuration workspace ...')
    
#Get Applications terraform configuration catalog 
tf_workspace_dirname = os.path.basename(TF_CONF_TEMPLATE.strip("/")) + '_' + context['SERVICEINSTANCEID']
    
src = TF_CONF_TEMPLATE
 #Check if the Applications catalog (src) exists.
if not os.path.exists(src):
    MSA_API.task_error('The Applications Terraform configuration is not found: ' + src, context)

#e.g: /opt/fmc_repository/Datafiles/CCLA/Terraform/APPLICATIONS/Workspaces/CLAA9/terraform-provision-aks-cluster
dest = TF_APPLICATIONS_WORKSPACES_BASE_DIR + subtenant_ext_ref + '/' + tf_workspace_dirname
context.update(terraform_provision_app_workspace=dest)
#Check if the Applications was already copied to the dest.
if not os.path.exists(dest):
    destination = shutil.copytree(src, dest) 
        
MSA_API.task_success('The application Terraform workspace is created successfully.', context)
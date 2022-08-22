import os
import uuid
import re
import shutil
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration


dev_var = Variables()
context = Variables.task_call(dev_var)

subtenant_ext_ref = context['UBIQUBEID']
Orchestration = Orchestration(subtenant_ext_ref)
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

#Terraform workspace base directory in Repository datafiles
TF_INFRASTRUCTURES_WORKSPACES_BASE_DIR = '/opt/fmc_repository/Datafiles/CCLA/Terraform/Infrastructures/Workspaces/'
TF_CONF_TEMPLATE = '/opt/fmc_repository/Process/cloudclapp-wf/Terraform_Configuration_Templates/Infrastructures/Catalogs/gcp/terraform_provision_gke_cluster_gcp'

tf_workspace_dirname = os.path.basename(TF_CONF_TEMPLATE.strip("/")) + '_' + context['SERVICEINSTANCEID']

Orchestration.update_asynchronous_task_details(*async_update_list, f'Retrieve configuration workspace ...')
    
src = TF_CONF_TEMPLATE
#Check if the infrastructure catalog (src) exists.
if not os.path.exists(src):
    MSA_API.task_error('The Infrastructure Terraform configuration is not found: ' + src, context)

#e.g: /opt/fmc_repository/Datafiles/CCLA/Terraform/Infrastructures/Workspaces/CLAA9/terraform-provision-aks-cluster
dest = TF_INFRASTRUCTURES_WORKSPACES_BASE_DIR + subtenant_ext_ref + '/' + tf_workspace_dirname

#Check if the infrastructure was already copied to the dest.
if not os.path.exists(dest):
    destination = shutil.copytree(src, dest) 
    
context.update(terraform_provision_gke_cluster_workspace=dest)

ret = MSA_API.task_success('Workspace Created Succesfully.', context)
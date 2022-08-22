import os
import uuid
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
TF_INFRASTRUCTURES_BASE_DIR = '/opt/fmc_repository/Process/cloudclapp-wf/Terraform_Configuration_Templates/Infrastructures/'
TF_WORKSPACE_DIR = '/opt/fmc_repository/Datafiles/CCLA/Terraform_Workspaces'
TF_INFRASTRUCTURES_CATALOGS_DIR = TF_INFRASTRUCTURES_BASE_DIR + 'Catalogs/'
TF_CONFIG_AWS_EC2_DEFAULT_DIR_NAME = 'aws/terraform_provision_aws_ec2'
TF_CONFIG_AWS_EC2_DEFAULT_CATALOG = TF_INFRASTRUCTURES_CATALOGS_DIR + TF_CONFIG_AWS_EC2_DEFAULT_DIR_NAME
TF_AWS_EC2_DEFAULT_MAIN_CONFIG_FILENAME = ''

#Generate UUID to cancate to the TF_CONFIG_AKS_DEFAULT_DIR_NAME and allows to uniq identification.
tf_config_workspace_name_uuid = str(uuid.uuid4())

tf_workspace_dirname = TF_CONFIG_AWS_EC2_DEFAULT_DIR_NAME + '_' + tf_config_workspace_name_uuid

Orchestration.update_asynchronous_task_details(*async_update_list, f'Retrieve configuration workspace ...')
    
#Copy the TF infrastructure configuration from catalog to the terraform workspace dedicateed for the subtenant. 
#(e.g: /opt/fmc_repository/Datafiles/CCLA/Terraform/Infrastructures/Catalogs/terraform-provision-aks-cluster)
src = TF_CONFIG_AWS_EC2_DEFAULT_CATALOG
#e.g: /opt/fmc_repository/Datafiles/CCLA/Terraform/Infrastructures/Workspaces/CLAA9/terraform-provision-aks-cluster
dest = TF_WORKSPACE_DIR + '/' + subtenant_ext_ref + '/' + tf_workspace_dirname
context.update(msa_dev_terraform_provision_aws_ec2_workspace=dest)
#Check if the infrastructure was already copied to the dest.
if not os.path.exists(dest):
    destination = shutil.copytree(src, dest) 
ret = MSA_API.task_success('Workspace Created Succesfully.', context)
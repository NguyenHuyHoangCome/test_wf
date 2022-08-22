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
dev_var.add('aws_region', var_type='String')
dev_var.add('aws_access_key_id', var_type='String')
dev_var.add('aws_secret_access_key', var_type='String')
dev_var.add('apps_to_deploy.0.aws_ami_id', var_type='String')
dev_var.add('apps_to_deploy.0.aws_instance_type', var_type='String')
dev_var.add('apps_to_deploy.0.aws_instance_name', var_type='String')
dev_var.add('tags.0.key', var_type='String')
dev_var.add('tags.0.value', var_type='String')
context = Variables.task_call(dev_var)

subtenant_ext_ref = context['UBIQUBEID']
Orchestration = Orchestration(subtenant_ext_ref)
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

#Terraform workspace base directory in Repository datafiles
TF_APPLICATIONS_BASE_DIR = '/opt/fmc_repository/Process/cloudclapp-wf/Terraform_Configuration_Templates/Applications/'
TF_WORKSPACE_DIR = '/opt/fmc_repository/Datafiles/CCLA/Terraform/Applications/Workspaces/'
TF_INFRASTRUCTURES_CATALOGS_DIR = TF_APPLICATIONS_BASE_DIR + 'Catalogs/'
TF_CONFIG_AWS_EC2_DEFAULT_DIR_NAME = 'aws/terraform_provision_vm-app_in_aws_ec2_vpc'
TF_CONFIG_AWS_EC2_DEFAULT_CATALOG = TF_INFRASTRUCTURES_CATALOGS_DIR + TF_CONFIG_AWS_EC2_DEFAULT_DIR_NAME
TF_AWS_EC2_DEFAULT_MAIN_CONFIG_FILENAME = ''

#Terraform workspace base directory in Repository datafiles
TF_APPLICATIONS_WORKSPACES_BASE_DIR = '/opt/fmc_repository/Datafiles/CCLA/Terraform/Applications/Workspaces/'
TF_CONF_TEMPLATE = '/opt/fmc_repository/Process/cloudclapp-wf/Terraform_Configuration_Templates/Applications/Catalogs/aws/terraform_provision_vm-app_in_aws_ec2_vpc'

if __name__ == "__main__":
    #Read 'APPLICATIONS/environments' description:
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Retrieve terraform configuration workspace ...')
    
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
        
    MSA_API.task_success('The Application Terraform workspace is created successfully.', context)
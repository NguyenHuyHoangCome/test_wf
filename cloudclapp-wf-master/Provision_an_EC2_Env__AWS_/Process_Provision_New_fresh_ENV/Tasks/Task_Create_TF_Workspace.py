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
TF_INFRASTRUCTURES_WORKSPACES_BASE_DIR = '/opt/fmc_repository/Datafiles/CCLA/Terraform/Infrastructures/Workspaces/'
TF_CONF_TEMPLATE = '/opt/fmc_repository/Process/cloudclapp-wf/Terraform_Configuration_Templates/Infrastructures/Catalogs/aws/terraform-provision-aws-ec2-vpc'

if __name__ == "__main__":
    #Read 'infrastructures/environments' description:
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Retrieve terraform configuration workspace ...')
    
    tf_workspace_dirname = os.path.basename(TF_CONF_TEMPLATE.strip("/")) + '_' + context['SERVICEINSTANCEID']
    
    #Copy the TF infrastructure configuration from catalog to the terraform workspace dedicateed for the subtenant. 
    #(e.g: /opt/fmc_repository/Datafiles/CCLA/Terraform/Infrastructures/Catalogs/Google/terraform-provision-eks-cluster)
    src = TF_CONF_TEMPLATE
    
    #Check if the infrastructure catalog (src) exists.
    if not os.path.exists(src):
        MSA_API.task_error('The Infrastructure Terraform configuration is not found: ' + src, context)
    
    #e.g: /opt/fmc_repository/Datafiles/CCLA/Terraform/Infrastructures/Workspaces/CLAA9/terraform-provision-eks-cluster
    dest = TF_INFRASTRUCTURES_WORKSPACES_BASE_DIR + subtenant_ext_ref + '/' + tf_workspace_dirname
    #Check if the infrastructure was already copied to the dest.
    if not os.path.exists(dest):
        destination = shutil.copytree(src, dest) 
    
    terraform_provision_ec2_vpc_workspace = dest
    context.update(terraform_provision_ec2_vpc_workspace=terraform_provision_ec2_vpc_workspace)
        
    MSA_API.task_success('The EKS Cluster Terraform workspace is created successfully.', context)
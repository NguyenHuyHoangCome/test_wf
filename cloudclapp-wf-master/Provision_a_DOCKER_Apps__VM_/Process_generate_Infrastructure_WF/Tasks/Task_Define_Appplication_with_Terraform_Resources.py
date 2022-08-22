import os
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
TF_APPLICATIONS_BASE_DIR = '/opt/fmc_repository/Datafiles/CCLA/Terraform/Applications/'
TF_APPLICATIONS_CATALOGS_DIR = TF_APPLICATIONS_BASE_DIR + 'Catalogs/'
TF_CONFIG_DOCKER_APP_DEFAULT_DIR_NAME = 'terraform_docker_container_compose_file_based'
TF_CONFIG_DOCKER_APP_DEFAULT_CATALOG = TF_APPLICATIONS_CATALOGS_DIR + TF_CONFIG_DOCKER_APP_DEFAULT_DIR_NAME
#WARNING: this terraform main configuration (e.g: aks-cluster.tf) can be changed according the catalog.
TF_DOCKER_APP_DEFAULT_MAIN_CONFIG_FILENAME = 'remote_command.tf'

if __name__ == "__main__":
    #Read 'applications/environments' description:
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Retrieve terraform configuration workspace ...')
    
    #check if terraform git url is defined in the environment descriptor. 
    applications_descriptor = context.get('applications_descriptor')
    if 'url' in applications_descriptor and applications_descriptor.get('url'):
        #git clone applications_descriptor.get('url') to TF_WORKSPACE_BASE_DIR + context['UBIQUBEID'] 
        pass
    else:
        #Copy the TF infrastructure configuration from catalog to the terraform workspace dedicateed for the subtenant. 
        #(e.g: /opt/fmc_repository/Datafiles/CCLA/Terraform/Applications/Catalogs/terraform-provision-aks-cluster)
        src = TF_CONFIG_DOCKER_APP_DEFAULT_CATALOG
        #e.g: /opt/fmc_repository/Datafiles/CCLA/Terraform/Applications/Workspaces/CLAA9/terraform-provision-aks-cluster
        dest = TF_APPLICATIONS_BASE_DIR + 'Workspaces/' + subtenant_ext_ref + '/' + TF_CONFIG_DOCKER_APP_DEFAULT_DIR_NAME + '/'
        context.update(msa_dev_terraform_provision_aks_cluster_workspace=dest)
        #Check if the infrastructure was already copied to the dest.
        if not os.path.exists(dest):
            destination = shutil.copytree(src, dest) 
        
        #terraform_provision_aks_cluster_workspace = dst + '/' + TF_CONFIG_DOCKER_APP_DEFAULT_DIR_NAME + '/' + TF_DOCKER_APP_DEFAULT_MAIN_CONFIG_FILENAME
        
        '''
        WARNING: as terraform is currently installed in the MSA docker containers host. The TF configuration workspace 'terraform_provision_aks_cluster' path 
        will be set in context the based-on docker instances volumes absolute path (e.g: /var/lib/docker/volumes/quickstart_msa_repository/_data/Datafiles/CCLA/Terraform/Applications/Workspaces/CLA9/)
        '''
        volume_base_dir = '/var/lib/docker/volumes/quickstart_msa_repository/_data/Datafiles/CCLA/Terraform/Applications/Workspaces'
        #volume_base_dir = '/opt/fmc_repository/Datafiles/CCLA/Terraform/Applications/Workspaces'
        terraform_provision_docker_app_workspace = volume_base_dir + '/' + subtenant_ext_ref + '/' + TF_CONFIG_DOCKER_APP_DEFAULT_DIR_NAME + '/' + TF_DOCKER_APP_DEFAULT_MAIN_CONFIG_FILENAME
        
        context.update(terraform_provision_docker_app_workspace=terraform_provision_docker_app_workspace)
        
    ret = MSA_API.task_success('The Application Terraform Resources definition is done successfully (copy locally into '+terraform_provision_docker_app_workspace +')', context)
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

if __name__ == "__main__":
    if 'terraform_provision_app_workspace' in context:
        #Read 'infrastructures/environments' description:
        Orchestration.update_asynchronous_task_details(*async_update_list, f'Romeving AKS cluster terraform workspace ...')
        #Get the terraform AKS provisioning workspace
        terraform_provision_aks_cluster_workspace = context.get('terraform_provision_app_workspace')
        #Check if the infrastructure was already copied to the dest.
        if os.path.exists(terraform_provision_aks_cluster_workspace):
            destination = shutil.rmtree(terraform_provision_aks_cluster_workspace)
        
        Orchestration.update_asynchronous_task_details(*async_update_list, f'Romeving AKS cluster terraform workspace ...OK')
    
    ret = MSA_API.task_success('The service is deleted successfully.', context)
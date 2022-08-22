import re
import subprocess
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants
from msa_sdk.device import Device
from msa_sdk.orchestration import Orchestration
from msa_sdk import util

dev_var = Variables()
context = Variables.task_call(dev_var)

'''
allows to get terraform output resource value.
'''
def get_tf_output_value(tf_workspace, resource_name, Orchestration):
    #Prepare command as list.
    tf_chdir = '-chdir=' + tf_workspace
    command = ['terraform',tf_chdir,'output','-raw', resource_name]
    #execute command.
    ret = terraform_run(command, Orchestration)
    return ret

'''
Allows execution of terraform locaaly.
'''
def terraform_run(command, Orchestration, check_stderr=False):
    output = ''
    ret = ''
    if check_stderr:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    else:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True)
    while True:
        output += process.stdout.readline()
        Orchestration.update_asynchronous_task_details(*async_update_list, output.strip())
        # Do something else
        return_code = process.poll()
        if return_code is not None:
            # Process has finished, read rest of the output 
            if output:
                for output in process.stdout.readlines():
                    ret += output + "\n"
                    Orchestration.update_asynchronous_task_details(*async_update_list, ret.strip())
                break
            else:
                for output in process.stderr.readlines():
                    ret += output + "\n"
                    Orchestration.update_asynchronous_task_details(*async_update_list, ret.strip())
                break
    ret += output
    return ret

subtenant_ext_ref = context['UBIQUBEID']
Orchestration = Orchestration(subtenant_ext_ref)
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

if __name__ == "__main__":
    
    #Terraform refresh
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Terraform refresh status ...')
    #Tf work directory definition
    work_directory = context.get('terraform_provision_aks_cluster_workspace')
    tf_chdir = '-chdir=' + work_directory 
    #Prepare tf plan command
    plan_output = 'terraform.plan.output'
    
    ### Get K8s cluster resource_group_name
    resource_group_name = get_tf_output_value(work_directory, 'resource_group_name', Orchestration)
    context.update(resource_group_name=resource_group_name)
    ### Get K8s cluster kubernetes_cluster_name
    kubernetes_cluster_name = get_tf_output_value(work_directory, 'kubernetes_cluster_name', Orchestration)
    context.update(kubernetes_cluster_name=kubernetes_cluster_name)
    
    #Tf work directory definition
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Configure AKS Dashbord access ...')
    
    access_k8s_dashboard = "https://portal.azure.com/#resource/subscriptions/"+context.get('service_principal_subscription_id')+"/resourceGroups/"+context.get('resource_group_name')+"/providers/Microsoft.ContainerService/managedClusters/"+context.get('kubernetes_cluster_name')+"/workloads"
    context.update(access_k8s_dashboard=access_k8s_dashboard)
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Retrieve AKS Dashbord URL access ...OK')
    
    MSA_API.task_success('The AKS dashboard is now available by clicking on the "Access to AKS Dashboard" link.' + access_k8s_dashboard, context)
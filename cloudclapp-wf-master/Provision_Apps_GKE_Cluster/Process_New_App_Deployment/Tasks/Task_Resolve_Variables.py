import re
import subprocess
import os
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration
from msa_sdk.device import Device
from msa_sdk import util

dev_var = Variables()
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
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    #Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

'''
allows to get configuration variable value.
'''
def _get_configuration_variable(device, name):
    value = ''
    ret = device.get_configuration_variable(name)
    if 'value' in ret:
        value = ret.get('value')
        return value
    return ''

'''
Allows execution of terraform localy.
'''
def terraform_run(command, Orchestration):
    output = ''
    ret = ''
    process = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True)
    while True:
        output += process.stdout.readline()
        #Orchestration.update_asynchronous_task_details(*async_update_list, output.strip())
        # Do something else
        return_code = process.poll()
        if return_code is not None:
            # Process has finished, read rest of the output 
            for output in process.stdout.readlines():
                ret += output + "\n"
                #Orchestration.update_asynchronous_task_details(*async_update_list, ret.strip())
            break
    return ret + output

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
    
def form_app_file(work_directory, app_name, app_image, app_port, app_replicas, app_node_port):
    app_file = work_directory +"/app.tf"
    with open(app_file) as f:
    	newText=f.read().replace('app_deploy', app_name+"_deploy")
    	newText = newText.replace('app_name', app_name)
    	newText = newText.replace('app_image', app_image)
    	newText = newText.replace('app_label', app_name)
    	newText = newText.replace('app_replicas', app_replicas)
    	newText = newText.replace('app_container_name', app_name)
    	newText = newText.replace('app_port', app_port)
    	newText = newText.replace('app_service', app_name+"_service")
    	newText = newText.replace('app-service', app_name+"-service")
    	if app_node_port is not None:
    		newText = newText.replace('#node_port', 'node_port')
    		newText = newText.replace('app_node_port', app_node_port)
    	newText = newText.replace('app_lb_ip', app_name+"_lb_ip")
    new_app_file = work_directory +"/"+app_name+".tf"
    with open(new_app_file, "w") as f:
    	f.write(newText)

#Variables.
subtenant_ext_ref = context['UBIQUBEID']
Orchestration = Orchestration(subtenant_ext_ref)
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

#Terraform file where the inputs variables will be field in therraform workspace.
TERRAFORM_TFVARS_FILENAME = "terraform.tfvars"
TERRAFORM_EKS_CLUSTER_STATE_FILENAME = "terraform.tfstate"


if __name__ == "__main__":
    #Retrieve AKS Cluster authentification informations from infrastructure Managed Entity configuration variables.
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Retrieve AKS Cluster authenefication details ...')
    #Get AKS Cluster ME external reference.
    device_ext_ref = context.get('env_infrastructure_me')
    if not device_ext_ref:
        MSA_API.task_error('The AKS Cluster Managed Entity is missing from input variables.', context)
    
    #Intialize Device from device ID:
    device_id = device_ext_ref[3:]
    device = Device(device_id=device_id)
    
    #Get configuration variables from infrastructure ME.
    cluster_name = _get_configuration_variable(device, 'cluster_name')
    
    #get work_directory from device configuration config
    cluster_tf_work_directory = _get_configuration_variable(device, 'cluster_tf_chdir')
    
    #Insert in variables in context.
    context.update(cluster_name=cluster_name)
    context.update(cluster_tf_work_directory=cluster_tf_work_directory)
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Retrieve AKS Cluster authenefication details ...OK')
    
    #Resolve variable into terraform.tfvars
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Resolve TF variables ...')
    
    #Provision EKS cluster terraform configuration filename.
    terraform_provision_app_workspace = context.get('terraform_provision_app_workspace')
    
    #Application terraform.tfvars filename.
    ftvars_filename = terraform_provision_app_workspace +"/"+ TERRAFORM_TFVARS_FILENAME
    #EKS cluster terraform.tfvars filename
    cluster_terraform_remote_state = cluster_tf_work_directory +"/"+ TERRAFORM_EKS_CLUSTER_STATE_FILENAME
    set_tfconfig_variable_value(ftvars_filename, 'cluster_terraform_remote_state', cluster_terraform_remote_state, context)
    
    apps_to_deploy = context.get('apps_to_deploy')
    
    for app in apps_to_deploy:
    	app_node_port = None
    	if 'app_node_port' in app.keys():
    		app_node_port = app['app_node_port']
    	form_app_file(terraform_provision_app_workspace, app['app_name'], app['app_image'], app['app_port'], app['app_replicas'], app_node_port)
    os.remove(terraform_provision_app_workspace+"/app.tf")

    Orchestration.update_asynchronous_task_details(*async_update_list, f'Resolve TF variables ...OK')
    
    MSA_API.task_success('The terraform variables are updated successfully.', context)
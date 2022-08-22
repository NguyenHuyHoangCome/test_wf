import subprocess
import os
import json
import shutil
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants
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
Allows execution of terraform localy.
'''
def terraform_run(command, Orchestration):
    output = ''
    ret = ''
    process = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True)
    while True:
        output = process.stdout.readline()
        util.log_to_process_file(context['SERVICEINSTANCEID'], output, context['PROCESSINSTANCEID'])
        # Do something else
        return_code = process.poll()
        if return_code is not None:
            # Process has finished, read rest of the output 
            for ret in process.stdout.readline():
                try:
                    util.log_to_process_file(context['SERVICEINSTANCEID'], ret.strip(), context['PROCESSINSTANCEID'])
                except TypeError:
                    continue
            break
        #else:
            #MSA_API.task_error('The TF init is failed: ' + ret , context)
    return ret

subtenant_ext_ref = context['UBIQUBEID']
Orchestration = Orchestration(subtenant_ext_ref)
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

if __name__ == "__main__":
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Execute terraform plan ...')
    #Tf work directory definition
    work_directory = context.get('terraform_provision_aks_cluster_workspace')
    tf_state_file = work_directory+"/terraform.tfstate"
    if not os.path.exists(work_directory+"/terraform.tfstate"):
    	shutil.rmtree(work_directory)
    	context.update(is_cluster_created=False)
    	MSA_API.task_success('No Cluster Created, Clearing Internal Entities', context)
    	sys.exit()
    tf_chdir = '-chdir=' + work_directory 
    #Prepare tf plan command
    plan_output = 'terraform.plan.output'
    tf_action = 'plan'
    tf_action_opt = '-out=' + plan_output
    #shell command as list.
    command = ['terraform', tf_chdir, tf_action, tf_action_opt]
    #execute terraform config.
    terraform_run(command, Orchestration)
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Execute terraform plan ...OK')
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Execute terraform destroy ...')
    #Prepare tf destroy command
    tf_action = 'destroy' 
    tf_action_opt = '-auto-approve'
    #shell command as list.
    command = ['terraform', tf_chdir, tf_action, tf_action_opt]
    #execute terraform config.
    terraform_run(command, Orchestration)
    
    with open(tf_state_file) as f:
    	state = json.load(f)
    	f.close()
    	if not state['resources']:
    		shutil.rmtree(work_directory)
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Execute terraform destroy ...OK')
    
    MSA_API.task_success('The destroying of the AKS Cluster is done successfully.', context)
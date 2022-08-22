import subprocess
import os
import shutil
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration
from msa_sdk import util

dev_var = Variables()
context = Variables.task_call(dev_var)

'''
Allows execution of terraform locaaly.
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

cluster_tf_work_directory = context.get('cluster_tf_work_directory')

service_account_key_file_path = cluster_tf_work_directory +"/service-account-key.json"

#configure gcloud sdk for authentication        
cmd = ["gcloud", "auth", "activate-service-account", "--key-file="+service_account_key_file_path]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
std_out, std_err = process.communicate()
if process.returncode != 0:
	output = process.stdout.read()
	if 'Activated service account' not in output:
		MSA_API.task_error(output, context)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account_key_file_path

if __name__ == "__main__":
    #Tf work directory definition
    work_directory = context.get('terraform_provision_app_workspace')
    tf_chdir = '-chdir=' + work_directory 
    tf_action = 'destroy' 
    tf_action_opt = '-auto-approve'
    #shell command as list.
    command = ['terraform', tf_chdir, tf_action, tf_action_opt]
    #execute terraform config.
    ret = terraform_run(command, Orchestration)
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Execute terraform destroy ...OK')
    
    MSA_API.task_success('The GKE Cluster Tear Down successfull.', context)
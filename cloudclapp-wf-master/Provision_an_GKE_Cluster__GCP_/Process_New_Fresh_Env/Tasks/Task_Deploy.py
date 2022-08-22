import subprocess
import os
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
    return output + ret

subtenant_ext_ref = context['UBIQUBEID']
Orchestration = Orchestration(subtenant_ext_ref)
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])
client_certificate_value = str(context.get('gcp_service_account_email')).replace("@","%40")
workspace_dir = context.get('terraform_provision_gke_cluster_workspace')
service_account_file = workspace_dir + "/service-account-key.json"
with open(service_account_file) as f:
    newText = f.read().replace('project_id_value', context.get('gcp_project_id'))
    newText = newText.replace('private_key_id_value', str(context.get('gcp_private_key_id')))
    newText = newText.replace('private_key_value', context.get('gcp_private_key'))
    newText = newText.replace('client_email_value', str(context.get('gcp_service_account_email')))
    newText = newText.replace('client_id_value', context.get('gcp_client_id'))
    newText = newText.replace('client_certificate_value', client_certificate_value)
    
with open(service_account_file, "w") as f:
    f.write(newText)

#configure gcloud sdk for authentication        
cmd = ["gcloud", "auth", "activate-service-account", "--key-file="+service_account_file]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
std_out, std_err = process.communicate()
if process.returncode != 0:
	output = process.stdout.read()
	if 'Activated service account' not in output:
		MSA_API.task_error(output, context)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account_file
os.environ['GOOGLE_PROJECT'] = context.get('gcp_project_id')

if __name__ == "__main__":
    #Tf work directory definition
    work_directory = context.get('terraform_provision_gke_cluster_workspace')
    tf_chdir = '-chdir=' + work_directory 
    command = ['terraform', tf_chdir, 'fmt']
    terraform_run(command, Orchestration)
    
    command = ['terraform', tf_chdir, 'init']
    terraform_run(command, Orchestration)
    
    command = ['terraform', tf_chdir, 'validate']
    terraform_run(command, Orchestration)
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Execute terraform plan ...')
    #Prepare tf plan command
    plan_output = 'terraform.plan.output'
    tf_action = 'plan'
    tf_action_opt = '-out=' + plan_output
    #shell command as list.
    command = ['terraform', tf_chdir, tf_action, tf_action_opt]
    #execute terraform config.
    terraform_run(command, Orchestration)
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Execute terraform plan ...OK')
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Execute terraform apply ...')
    #Prepare tf apply command
    tf_action = 'apply' 
    tf_action_opt = '-auto-approve'
    #shell command as list.
    command = ['terraform', tf_chdir, tf_action, tf_action_opt, plan_output]
    #execute terraform config.
    terraform_run(command, Orchestration)
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Execute terraform apply ...OK')
    
    MSA_API.task_success('The GKE Cluster provisioned successfully.', context)
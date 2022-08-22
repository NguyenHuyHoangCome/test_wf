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

def get_tf_output_value(tf_workspace, resource_name, Orchestration):
    #Prepare command as list.
    tf_chdir = '-chdir=' + tf_workspace
    command = ['terraform',tf_chdir,'output','-raw', resource_name]
    #execute command.
    ret = terraform_run(command, Orchestration)
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
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Execute terraform plan ...')
    #Tf work directory definition
    work_directory = context.get('terraform_provision_app_workspace')
    tf_chdir = '-chdir=' + work_directory 
    
    command = ['terraform', tf_chdir, 'fmt']
    terraform_run(command, Orchestration)
    
    command = ['terraform', tf_chdir, 'init']
    terraform_run(command, Orchestration)
    
    command = ['terraform', tf_chdir, 'validate']
    terraform_run(command, Orchestration)
    
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
    
    apps_to_deploy = context.get('apps_to_deploy')
    
    for app in apps_to_deploy:
    	app_ip = get_tf_output_value(work_directory, app['app_name']+"_lb_ip", Orchestration)
    	index = apps_to_deploy.index(next(filter(lambda n: n.get('app_name') == app['app_name'], apps_to_deploy)))
    	context['apps_to_deploy'][index]['app_access'] = app_ip+" : "+app['app_port']
    
    MSA_API.task_success('The application is deployed successfully.', context)
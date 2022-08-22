import subprocess
import pexpect
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration
from jproperties import Properties
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

def aws_configure(work_directory):
    configs = Properties()
    var_file = work_directory+"/terraform.tfvars"
    with open(var_file, 'rb') as config_file:
    	configs.load(config_file)
    	aws_access_key = configs.get('access_key').data.strip('"')
    	aws_secret_key = configs.get('secret_key').data.strip('"')
    child = pexpect.spawn('aws configure')
    child.expect(':')
    child.sendline(aws_access_key)
    child.expect(':')
    child.sendline(aws_secret_key)
    child.expect(':')
    child.sendline('')
    child.expect(':')
    child.sendline('')
    child.expect(pexpect.EOF, timeout=None)
    return None

subtenant_ext_ref = context['UBIQUBEID']
Orchestration = Orchestration(subtenant_ext_ref)
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

if __name__ == "__main__":
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Execute terraform plan ...')
    #Tf work directory definition
    work_directory = context.get('terraform_provision_app_workspace')
    cluster_tf_work_directory = context.get('cluster_tf_work_directory')
    aws_configure(cluster_tf_work_directory)
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
    	app_ip = get_tf_output_value(work_directory, app['app_name']+"_load_balancer_hostname", Orchestration)
    	index = apps_to_deploy.index(next(filter(lambda n: n.get('app_name') == app['app_name'], apps_to_deploy)))
    	context['apps_to_deploy'][index]['app_access'] = app_ip+" : "+app['app_port']

    MSA_API.task_success('The application is deployed successfully.', context)
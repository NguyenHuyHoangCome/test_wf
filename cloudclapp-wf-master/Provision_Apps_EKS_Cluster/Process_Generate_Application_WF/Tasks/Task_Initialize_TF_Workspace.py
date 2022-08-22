import subprocess
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

if __name__ == "__main__":
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Execute terraform init ...')
    #Prepare tf plan command
    work_directory = context.get('terraform_provision_app_workspace')
    tf_chdir = '-chdir=' + work_directory 
    tf_action = 'init'
    command = ['terraform', tf_chdir, tf_action]
    output = terraform_run(command, Orchestration)
    context.update(output=output)
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Execute terraform init ...OK')
    
    MSA_API.task_success('The application terraform workspace init is done successfully: ' + output , context)
import json
from msa_sdk import constants
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.orchestration import Orchestration

dev_var = Variables()
context = Variables.task_call(dev_var)


Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

if __name__ == "__main__":
    #Read 'infrastructures/environments' description:
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Read the applications definitions from descriptor...')
    
    DESC_APPLICATIONS = 'applications'
    applications = list()
    if 'description_dict' in context:
        description_dict = context.get('description_dict')
        if DESC_APPLICATIONS in description_dict:
            applications = description_dict.get(DESC_APPLICATIONS)
            #insert applications descriptors into the context
            context.update(applications_descriptor=applications)
    apps_json = json.dumps(applications)
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Read the applications definitions from descriptor...OK')
    
    #Finish the task
    ret = MSA_API.task_success('Success. Workflow allows to generate applications TF configuration is created: ' + apps_json, context)
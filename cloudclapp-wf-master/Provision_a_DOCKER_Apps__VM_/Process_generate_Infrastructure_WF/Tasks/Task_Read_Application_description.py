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
    #Read 'Applicationss/applications' description:
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Read the applications definition from descriptor...')
    
    DESC_APPLICATIONS = 'applications'
    applications = list()
    if 'description_dict' in context:
        description_dict = context.get('description_dict')
        if DESC_APPLICATIONS in description_dict:
            applications = description_dict.get(DESC_APPLICATIONS)
            #insert applications descriptor into the context.
            context.update(applications_descriptor=applications)
    
    infra_json = json.dumps(applications)
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Read the applications definition from descriptor...OK')
    
    #Finish the task
    ret = MSA_API.task_success('Success. Workflow allows to generate Application TF configuration is created: ' + infra_json, context)
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
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Read the infrastructures definition from descriptor...')
    
    DESC_ENVIRONMENTS = 'environments'
    infrastructures = list()
    if 'description_dict' in context:
        description_dict = context.get('description_dict')
        if DESC_ENVIRONMENTS in description_dict:
            infrastructures = description_dict.get(DESC_ENVIRONMENTS)
            #insert infrastructures descriptor into the context.
            context.update(infrastructures_descriptor=infrastructures)
    
    infra_json = json.dumps(infrastructures)
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Read the infrastructures definition from descriptor...OK')
    
    #Finish the task
    ret = MSA_API.task_success('Success. Workflow allows to generate Infrastructure TF configuration is created: ' + infra_json, context)
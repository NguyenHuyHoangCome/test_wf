import json
from msa_sdk import constants
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.orchestration import Orchestration

dev_var = Variables()
dev_var.add('descriptor', var_type='String')
context = Variables.task_call(dev_var)

'''
Read file content.
'''
def read_json_descriptor_content(filename, context):
    try:
        with open(filename, 'r') as file:
            data = file.read().replace('\n', '')
            return data
    except FileNotFoundError:
        MSA_API.task_error('The descriptor file is not found here: ' + filename, context)
    except:
        MSA_API.task_error('Failed to read the descriptor file.', context)

Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

if __name__ == "__main__":
    #Check the descriptor format.
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Check the descriptor format...')
    
    description = ""
    if 'descriptor' in context:
        description = context.get('descriptor')
        #check if descriptor is a JSON as string or YAML file.
        if description.lower().endswith('.json'):
            description_json = read_json_descriptor_content(description, context)
            description_dict = json.loads(description_json)
            #insert description as dictionnry into the context.
            context.update(description_dict=description_dict)
        elif description.lower().endswith('.yaml', 'yml'):
            #TODO: implement code to handle YAML descriptor file from repository.
            pass
        else:
            MSA_API.task_error('The descriptor format is support, JSON as string and YAML file path is expetced.', context)
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Check the descriptor format... OK')
    
    #Finish the task
    ret = MSA_API.task_success('The service is created successfully.', context)
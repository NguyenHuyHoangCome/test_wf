import json
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration

dev_var = Variables()
context = Variables.task_call(dev_var)

'''
Retrieve process instance by service instance ID.

@param orch:
    Ochestration class object reference.
@param process_id:
    Baseline workflow process ID.
@param timeout:
    loop duration before to break.
@param interval:
    loop time interval.
@return:
    Response of the get process instance execution.
'''
def get_process_instance(orch, process_id, timeout = 600, interval=5):
    response = {}
    global_timeout = time.time() + timeout
    while True:
        #get service instance execution status.
        orch.get_process_instance(process_id)
        response = json.loads(orch.content)
        status = response.get('status').get('status')
        #context.update(get_process_instance=status)
        if status != constants.RUNNING or time.time() > global_timeout:
            break
        time.sleep(interval)

    return response

def _execute_service_by_service_id(orch, context, subtenant_ext_ref, process_name, data):
    #get service external ref
    service_ext_ref = context.get('tfw_service_instance_dict').get('external_ref')
    tfw_service_instance_id = context.get('tfw_service_instance_dict').get('instance_id')

    #service name
    service_name = context.get('tf_wf_service_name')
    #execute service by ref.
    if isinstance(data, dict):
        #orch.execute_service_by_reference(subtenant_ext_ref, service_ext_ref, service_name, process_name, data)
        orch.execute_launch_process_instance(tfw_service_instance_id, process_name, data)

        response = json.loads(Orchestration.content)
        context.update(response_execute_service_by_service_id=response)
        process_id = response.get('processId').get('id')
        service_id = response.get('serviceId').get('id')
        
        #get service process details.
        response = get_process_instance(Orchestration, process_id)
        status = response.get('status').get('status')
        details = response.get('status').get('details')
        if status == constants.FAILED:
            MSA_API.task_error( 'Execute service operation is failed: ' + details + ', (#' + str(service_id) + ')',context , True)

    
subtenant_ext_ref = context['UBIQUBEID']
Orchestration = Orchestration(subtenant_ext_ref)
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

if __name__ == "__main__":
    #Get Terraform device external reference from context (e.g: UBI2455).
    tf_device_id = context.get('tf_device_id')
    
    #Empty data as dictionnary for terraform plan and apply 
    data = dict()
    
    #Plan Terraform configuration provision.
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Execute Terraform Plan ...')
    
    _execute_service_by_service_id(Orchestration, context, subtenant_ext_ref, 'Process_Plan', data)
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Execute Terraform Plan ...OK')
    
    #Apply Terraform configuration provision.
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Execute Terraform Apply ...')
    
    _execute_service_by_service_id(Orchestration, context, subtenant_ext_ref, 'Process_Apply', data)
    
    Orchestration.update_asynchronous_task_details(*async_update_list, f'Execute Terraform Apply ...OK')
        
    ret = MSA_API.task_success('The provisioning of the Terraform (plan + apply) is done successfully.', context)
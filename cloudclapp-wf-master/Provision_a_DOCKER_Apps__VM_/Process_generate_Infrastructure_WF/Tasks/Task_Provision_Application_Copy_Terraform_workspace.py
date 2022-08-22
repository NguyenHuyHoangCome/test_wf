import json
import time
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants
from msa_sdk.orchestration import Orchestration

dev_var = Variables()
dev_var.add('tf_device_id', var_type='Device')

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


subtenant_ext_ref = context['UBIQUBEID']
Orchestration = Orchestration(subtenant_ext_ref)
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])

if __name__ == "__main__":
    #Get Terraform device external reference from context (e.g: UBI2455).
    #tf_device_id = 'ClO151'
    tf_device_id = context['tf_device_id']
    #tf_device_id = tf_device_ref[3:]
    
    #Terraform_Configuration_Management WF service name constant variable.
    SERVICE_NAME = 'Process/Terraform_Configuration_Management/Terraform_Configuration_Management'
    CREATE_PROCESS_NAME = 'Process_New_Instance'
    COPY_PROCESS_NAME = 'Process_Copy'
    service_id = ''
    service_ext_ref = ''
    context.update(tf_wf_service_name=SERVICE_NAME)
    #Provision AKS cluster terraform configuration filename.
    terraform_provision_docker_app_workspace = context.get('terraform_provision_docker_app_workspace') #/var/lib/docker/volumes/quickstart_msa_repository/_data/Datafiles/CCLA/Terraform/Applications/Workspaces/ClOA10/terraform_docker_container_compose_file_based"

    src_configuration_file =  context.get('msa_dev_terraform_provision_aks_cluster_workspace') # "/opt/fmc_repository/Datafiles/CCLA/Terraform/Applications/Workspaces/ClOA10/terraform_docker_container_compose_file_based/",
    
    data = dict(device_id=tf_device_id, configuration_file=terraform_provision_docker_app_workspace, src_configuration_file=src_configuration_file)
    #Instantiate new  WF dedicated for the device_id.
    if not 'tfw_service_instance_dict' in context:
        if isinstance(data, dict):
            Orchestration.execute_service(SERVICE_NAME, CREATE_PROCESS_NAME, data)
            response = json.loads(Orchestration.content)
            process_id = response.get('processId').get('id')
            #get service process details.
            response = get_process_instance(Orchestration, process_id)
            status = response.get('status').get('status')
            details = response.get('status').get('details')
            if status == constants.ENDED:
                context['response'] = response
                if 'serviceId' in response:
                    service_id = response.get('serviceId').get('id')
                    service_ext_ref = response.get('serviceId').get('serviceExternalReference')
                    #Store service_instance_id of Terraform_Configuration_Management WF in context.
                    context['tfw_service_instance_dict'] = dict(external_ref=service_ext_ref, instance_id=service_id)
                else:
                    MSA_API.task_error('Missing service id return by orchestration operation, (#' + str(service_id) + ')',context , True)
        
            else:
                MSA_API.task_error('Execute service operation failed, (#' + str(service_id) + ')',context , True)
    
    #Initialize Terraform workspace.
    #  "tfw_service_instance_dict": {
    #     "external_ref": "ClOSID1374",
    #    "instance_id": 1374
    
    service_ext_ref = context.get('tfw_service_instance_dict').get('external_ref')
    tfw_service_instance_id = context.get('tfw_service_instance_dict').get('instance_id')
    
    if isinstance(data, dict):
        Orchestration.execute_launch_process_instance(tfw_service_instance_id, COPY_PROCESS_NAME, data)

        response = json.loads(Orchestration.content)
        context.update(response_execute_service_by_reference=response)
        process_id = response.get('processId').get('id')
        service_id = response.get('serviceId').get('id')
        
        #get service process details.
        response = get_process_instance(Orchestration, process_id)
        status = response.get('status').get('status')
        details = response.get('status').get('details')
        if status == constants.FAILED:
            MSA_API.task_error( 'Execute service operation is failed: ' + details + ', (#' + str(service_id) + ')',context , True)

MSA_API.task_success('The files are copied to the Terraform server successfully.', context) 
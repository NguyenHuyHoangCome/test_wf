from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import constants

dev_var = Variables()
context = Variables.task_call(dev_var)

ret = MSA_API.task_success('The AKS cluster provisioning is done successfully.', context)
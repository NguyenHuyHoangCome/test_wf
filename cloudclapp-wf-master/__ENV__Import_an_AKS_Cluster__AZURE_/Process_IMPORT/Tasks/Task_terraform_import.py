import os

from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

if __name__ == "__main__":

    context = Variables.task_call()
        
    # (4) Terrafrom import
    ADDR     = context["tf_object_addr"]
    ID       = context["tf_object_id"]
    work_dir = context["work_dir"]
    try:
        stream = os.popen(f'terraform -chdir="{work_dir}" import {ADDR} {ID}')
        terraform_res_02 = stream.read().strip("\n")
    except Exception as e:
        ret = MSA_API.process_content('WARNING', f'CAN\'T IMPORT TERRAFORM OBJECT ADDR: <<{ADDR}>>, ID: <<{ID}>>. ERROR: {e}', context, True)
        print(ret)
        exit()
        
    ret = MSA_API.process_content('ENDED', f'Terraform: {terraform_res_02}', context, True)
    print(ret)
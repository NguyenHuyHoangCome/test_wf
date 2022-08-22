import os

from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

if __name__ == "__main__":

    context = Variables.task_call()

    # (3) Terrafrom init
    work_dir = context["work_dir"]
    try:
        stream = os.popen(f'terraform -chdir="{work_dir}" init')
        terraform_res_01 = stream.read().strip("\n")
    except Exception as e:
        ret = MSA_API.process_content('WARNING', f'CAN\'T INIT TERRAFORM: {e}', context, True)
        print(ret)
        exit()
        
    ret = MSA_API.process_content('ENDED', f'Terraform: {terraform_res_01}', context, True)
    print(ret)
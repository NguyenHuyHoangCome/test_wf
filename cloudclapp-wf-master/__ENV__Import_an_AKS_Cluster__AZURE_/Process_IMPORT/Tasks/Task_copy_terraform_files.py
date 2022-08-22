import uuid
from shutil import copytree

from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

if __name__ == "__main__":

    context = Variables.task_call()

    # (2) Copy files into newly created directory
    work_dir = "/tmp/" + uuid.uuid4().hex
    src_dir  = context['src_dir']
    try:
        copytree(src_dir, work_dir)
    except Exception as e:
        ret = MSA_API.process_content('WARNING', f'CAN\'T COPY FILES: {e}', context, True)
        print(ret)
        exit()
        
    context["work_dir"] = work_dir
        
    ret = MSA_API.process_content('ENDED', f'Terraform files copied to <<{work_dir}>>', context, True)
    print(ret)
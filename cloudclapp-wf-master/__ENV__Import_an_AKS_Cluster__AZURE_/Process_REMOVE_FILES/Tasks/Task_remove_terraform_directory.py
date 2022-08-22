import os
import shutil

from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

if __name__ == "__main__":

    context = Variables.task_call()

    # (0) remove directory
    work_dir = context["work_dir"]
    try:
        # os.rmdir(dir_path)
        shutil.rmtree(work_dir)
    except OSError:
        ret = MSA_API.process_content('WARNING', f'CAN\'T REMOVE DIRECTORY <<{work_dir}>>', context, True)
        print(ret)
        exit()

    ret = MSA_API.process_content('ENDED', f'Directory removed <<{work_dir}>> - OK', context, True)
    print(ret)
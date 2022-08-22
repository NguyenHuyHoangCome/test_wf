import os

from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

if __name__ == "__main__":

    dev_var = Variables()
    dev_var.add('src_dir')
    dev_var.add('tf_object_addr')
    dev_var.add('tf_object_id')
    context = Variables.task_call(dev_var)

    # (0) Check TF files exist
    src_dir = context['src_dir']
    if not os.path.isdir(src_dir):
        ret = MSA_API.process_content('WARNING', f'Directory <<{src_dir}>> not found.', context, True)
        print(ret)
        exit()

    ret = MSA_API.process_content('ENDED', f'Checked directory <<{src_dir}>> - OK.', context, True)
    print(ret)
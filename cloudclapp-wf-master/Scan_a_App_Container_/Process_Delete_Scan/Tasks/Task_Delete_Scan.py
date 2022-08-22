import os
import shutil
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API


dev_var = Variables()

context = Variables.task_call(dev_var)
mydir = '/opt/fmc_repository/Datafiles/ccla_scan_app/'+context['UBIQUBEID']+"/"+context['SERVICEINSTANCEID']
shutil.rmtree(mydir)

ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)


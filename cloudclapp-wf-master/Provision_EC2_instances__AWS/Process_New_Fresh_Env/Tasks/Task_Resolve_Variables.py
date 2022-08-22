'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('aws_region', var_type='String')
dev_var.add('aws_access_key_id', var_type='String')
dev_var.add('aws_secret_access_key', var_type='String')
dev_var.add('ec2_instances.0.aws_ami_id', var_type='String')
dev_var.add('ec2_instances.0.aws_instance_type', var_type='String')
dev_var.add('ec2_instances.0.aws_instance_name', var_type='String')


context = Variables.task_call(dev_var)

workspace_dir = context.get('msa_dev_terraform_provision_aws_ec2_workspace')
tfvars_file = workspace_dir + "/terraform.tfvars"
with open(tfvars_file) as f:
    newText=f.read().replace('aws_region_value', context.get('aws_region'))
    newText = newText.replace('aws_access_key_id_value', context.get('aws_access_key_id'))
    newText = newText.replace('aws_secret_access_key_value', context.get('aws_secret_access_key'))
    
with open(tfvars_file, "w") as f:
    f.write(newText)
    
tfvars_template_file = workspace_dir + "/ec2_instance_tfvar_template"
ec2_instance_template_file = workspace_dir + "/ec2_instance_template"
ec2_instance_file = workspace_dir + "/ec2_instance.tf"

ec2_instances = context.get('ec2_instances')


    
i = 0
for ec2_instance in ec2_instances:
    with open(ec2_instance_template_file) as f:
        ec2_instance_content = f.read().replace('instance_no', str(i))
    with open(ec2_instance_file, "a") as f: 
        f.write(ec2_instance_content)
        f.write('\n')
    with open(tfvars_template_file) as f:
        ec2_instance_tfvars_content = f.read().replace('instance_no', str(i))
        ec2_instance_tfvars_content = ec2_instance_tfvars_content.replace('ec2_instances.'+str(i)+'.aws_ami_id_value', ec2_instance['aws_ami_id'])
        ec2_instance_tfvars_content = ec2_instance_tfvars_content.replace('ec2_instances.'+str(i)+'.aws_instance_type_value', ec2_instance['aws_instance_type'])
        ec2_instance_tfvars_content = ec2_instance_tfvars_content.replace('ec2_instances.'+str(i)+'.aws_instance_name_value', ec2_instance['aws_instance_name'])
    with open(tfvars_file, "a") as f:
        f.write(ec2_instance_tfvars_content)
        f.write('\n')
    i += 1
     
ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)


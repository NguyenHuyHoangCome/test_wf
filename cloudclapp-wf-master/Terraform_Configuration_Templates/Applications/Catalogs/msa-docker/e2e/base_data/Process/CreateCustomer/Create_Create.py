from msa_sdk.customer import Customer
from msa_sdk.variables import Variables

dev_var = Variables()
dev_var.add('name')
context = Variables.task_call(dev_var)

customer = Customer()
customer.create_customer_by_prefix('MSA', context['name'], 'MSA')

print(customer.process_content('ENDED', 'Task OK', context, True))
# HOW TO

## Workflow arguments

### <src_dir>
 - source directory, where the terrafrom files located (main.tf, terrafrom.tfvars etc.)
 - this directory should contain all the files required to allow terrafom make `init`, `plan`, `import` etc.

### <tf_object_addr>
 - terraform resource ADDR
 - example: `azurerm_resource_group.default` as it is named in terraform configuration files

### <tf_object_id>
 - terraform resource ID
 - ID assigned by MS Azure
 - example: `/subscriptions/<subscription-id>/resourcegroups/<resource-group-name>/providers/Microsoft.ContainerService/managedClusters/<resource-id-name>`  



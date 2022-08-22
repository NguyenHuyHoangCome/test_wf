# How to use

## Requirements
 - AKS cluster deployed

## Deployment
 - Configuration files are supposed to be used within `kubectl apply -f` command.
 - Check msa_front service configuration in Azure portal, and replace `type: ClusterIP` with `type: LoadBalancer`. Public `<ip-address>` will be allocated
 - MSA web-ui should be there `https://<ip-address>/`

## Notes
 - Adjust PVC (persistent volume claims) according to the project requirements (size and file permissions)
 - Replace msa_front container. Currently it points to private docker repo.

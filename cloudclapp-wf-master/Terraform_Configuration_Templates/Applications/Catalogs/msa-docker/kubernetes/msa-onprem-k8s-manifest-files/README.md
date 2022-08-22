# How to use

## Requirements
 - K8S cluster deployed
 - NFS server deployed

## Deployment
 - Configuration files are supposed to be used within `kubectl apply -f` command. You can use `deploy.sh` and `remove.sh` scripts.
 - Expose MSA web-ui through `kubectl port-forward --address 0.0.0.0 service/msa-front 65033:443`
 - MSA web-ui should be there `https://<k8s-ip>:65033`

## Notes
 - Adjust PV (persistent volumes) according to the project requirements (ip address, size and file permissions)
 - Replace msa_front container. Currently it points to private docker repo.

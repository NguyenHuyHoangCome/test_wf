# How to

## Requirements
 - install [helm](https://helm.sh/docs/intro/install/) - Current version v3.7.2
 - install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) - Current version v1.23.1 

## Variables
 - check values.yaml file and replace vaules if required

## Helm
 - To install chart run `helm install <app_name> . --namespace <namespace> --create-namespace --kubeconfig=<path_to_kubeconfig_file> --wait`
 - To remove chart `helm uninstall <app_name> --namespace <namespace> --kubeconfig=<path_to_kubeconfig_file>`
 - Remove namespace `kubectl delete ns <namespace> --kubeconfig=<path_to_kubeconfig_file>`

## Application
Application exposed on a NodePort `http://<node-port-ip>:30301` - once web page opened - text `Message` should appear, where:
 - `30301` - a node_port set in values.yaml

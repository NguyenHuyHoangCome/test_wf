# How to

## Variables
 - check terraform.tfvars file and replace vaules if required

## Terrafrom
 - run `terrafrom init`
 - run `terrafrom plan -out plan_01`
 - run `terrafrom apply "plan_01"`

## Application
Application exposed on a NodePort `http://<node-port-ip>:30300` - once web page opened - text `Message` should appear, where:
 - `30300` - a node_port set in terraform.tfvars
 - `Message` - a message set in terraform.tfvars
 - NodePort - an option set in main.tf - `kubernetes_service.front-end-svc`

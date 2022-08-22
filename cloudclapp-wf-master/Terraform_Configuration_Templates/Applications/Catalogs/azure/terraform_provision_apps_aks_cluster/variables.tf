variable "cluster_terraform_remote_state" {
  description = "EKS cluster terraform state file path"
}
variable "clientId" {
  description = "Azure Kubernetes Service Cluster service principal Client Id"
}

variable "clientSecret" {
  description = "Azure Kubernetes Service Cluster service principal Client Secret"
}

variable "subscriptionId" {
  description = "Azure Kubernetes Service Cluster service principal Subscription Id"
}

variable "tenantId" {
  description = "Azure Kubernetes Service Cluster service principal Tenant Id"
}

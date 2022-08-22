variable "gke_username" {
  default     = ""
  description = "gke username"
}

variable "gke_password" {
  default     = ""
  description = "gke password"
}

variable "project_id" {
  description = "project id"
}

variable "region" {
  description = "region"
}

variable "cluster_name" {
  description = "name of the cluster"
}

variable "gke_num_nodes" {
  default     = 2
  description = "number of gke nodes"
}

variable "vpc_name" {
  description = "name of the vpc"
}

variable "subnet_name" {
 description = "name of the subnet"
}

variable "ip_cidr_range" {
 description = "ip cidr range"
}

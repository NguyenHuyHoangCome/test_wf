variable "region" {
  default     = "us-east-2"
  description = "AWS region"
}

variable "access_key" {
  description = "AWS access key"
}

variable "secret_key" {
  description = "AWS secret key"
}

variable "vpc_name" {
  default     = "ec2-vpc-"
  description = "VPC Name"
}

variable "vpc_subnet" {
  default     = "10.0.0.0/16"
  description = "VPC subnet"
}

variable "private_subnets" {
  default     = ["10.0.1.0/24"]
  description = "VPC subnet"
}

variable "public_subnets" {
  default     = ["10.0.4.0/24"]
  description = "Public subnets"
}

variable "additional_tags" {
  description = "Additional resource tags"
  type        = map(string)
}


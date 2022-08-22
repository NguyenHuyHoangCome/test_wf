variable "region" {
  type = string
  description = "aws region"
}

variable "access_key" {
  type = string
  description = "aws access key id"
}

variable "secret_key" {
  type = string
  description = "aws secret access key"
}

variable "ec2_instances" {
   type = list(object({
    aws_ami_id = string
    aws_instance_type = string
    aws_instance_name = string
  }))
  description = "aws ec2 instance details"
}

variable "additional_tags" {
  default     = {"Project":"DEV_CLAA", "Team":"Automation"}
  description = "Additional resource tags"
  type        = map(string)
}

variable "vpc_id" {
  type = string
  description = "ec2 vpc id"
}

variable "security_group_id" {
  type = string
  description = "vpc default security group id"
}

variable "vpc_subnet_id" {
  type = string
  description = "vpc private subnet id"
}


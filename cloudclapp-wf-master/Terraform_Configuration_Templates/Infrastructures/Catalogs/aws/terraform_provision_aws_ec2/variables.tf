variable "aws_region" {
  type = string
  description = "aws region"
}

variable "aws_access_key_id" {
  type = string
  description = "aws access key id"
}

variable "aws_secret_access_key" {
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


output "region" {
  description = "AWS region"
  value       = var.region
}

output "vpc_id" {
  description = "VPC identifier"
  value       = module.vpc.vpc_id
}

output "vpc_name" {
  description = "AWS region"
  value       = module.vpc.name
}

output "private_subnets" {
  description = "Private subnets"
  value       = module.vpc.private_subnets
}

output "public_subnets" {
  description = "Private subnets"
  value       = module.vpc.public_subnets
}



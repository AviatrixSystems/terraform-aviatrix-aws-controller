output "private_ip" {
  value       = module.aviatrix_controller_build.private_ip
  description = "Private IP of the controller"
}

output "public_ip" {
  value       = module.aviatrix_controller_build.public_ip
  description = "Public IP of the controller"
}

output "vpc_id" {
  value       = module.aviatrix_controller_build.vpc_id
  description = "VPC where Aviatrix controller was built"
}

output "subnet_id" {
  value       = module.aviatrix_controller_build.subnet_id
  description = "Subnet where Aviatrix controller was built"
}

output "security_group_id" {
  value       = module.aviatrix_controller_build.security_group_id
  description = "Security group id used by Aviatrix controller"
}

output instance_id {
  value       = module.aviatrix_controller_build.instance_id
  description = "Controller instance ID"
}

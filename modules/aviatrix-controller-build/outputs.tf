output private_ip {
  value       = aws_instance.aviatrixcontroller.private_ip
  description = "Private IP of the controller"
}

output public_ip {
  value       = aws_eip.controller_eip.public_ip
  description = "Public IP of the controller"
}

output vpc_id {
  value       = data.aws_vpc.controller_vpc.id
  description = "VPC where Aviatrix controller was built"
}

output subnet_id {
  value       = data.aws_subnet.controller_subnet
  description = "Subnet where Aviatrix controller was built"
}

output security_group_id {
  value       = aws_security_group.AviatrixSecurityGroup.id
  description = "Security group id used by Aviatrix controller"
}

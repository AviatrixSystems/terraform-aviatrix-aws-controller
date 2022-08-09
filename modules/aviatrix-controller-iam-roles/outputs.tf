output "aws_account_id" {
  value       = data.aws_caller_identity.current.account_id
  description = "AWS account Id"
}

output "aviatrix_role_ec2_name" {
  value       = aws_iam_role.aviatrix_role_ec2.name
  description = "Aviatrix role name for EC2"
}

output "aviatrix_role_ec2_arn" {
  value       = aws_iam_role.aviatrix_role_ec2.arn
  description = "Aviatrix role ARN for EC2"
}

output "aviatrix_role_app_name" {
  value       = aws_iam_role.aviatrix_role_app.name
  description = "Aviatrix role name for application"
}

output "aviatrix_role_app_arn" {
  value       = aws_iam_role.aviatrix_role_app.arn
  description = "Aviatrix role ARN for application"
}

output "aviatrix_assume_role_policy_arn" {
  value       = aws_iam_policy.aviatrix_assume_role_policy.arn
  description = "Aviatrix assume role policy ARN"
}

output "aviatrix_app_policy_arn" {
  value       = aws_iam_policy.aviatrix_app_policy.arn
  description = "Aviatrix policy ARN for application"
}

output "aviatrix_role_ec2_profile_arn" {
  value       = aws_iam_instance_profile.aviatrix_role_ec2_profile.arn
  description = "Aviatrix role EC2 profile ARN for application"
}

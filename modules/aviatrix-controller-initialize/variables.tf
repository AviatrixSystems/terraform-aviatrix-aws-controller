data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

variable "controller_launch_wait_time" {
  type        = number
  description = "Controller launch wait time"
  default     = 210
}

variable "aws_account_id" {
  type        = string
  description = "aws account id"
  default     = ""
}

variable "public_ip" {
  type        = string
  description = "aviatrix controller public ip address(required)"
}

variable "private_ip" {
  type        = string
  description = "aviatrix controller private ip address(required)"
}

variable "admin_email" {
  type        = string
  description = "aviatrix controller admin email address"
}

variable "admin_password" {
  type        = string
  description = "aviatrix controller admin password"
}

variable "access_account_email" {
  type        = string
  description = "aviatrix controller access account email"
}

variable "controller_version" {
  type        = string
  default     = "latest"
  description = "The version in which you want launch Aviatrix controller"
}

variable "access_account_name" {
  type        = string
  description = "Access account name"
}

variable "customer_license_id" {
  type        = string
  description = "aviatrix customer license id"
  default     = ""
}

variable "ec2_role_name" {
  type        = string
  description = "EC2 role name"
  default     = ""
}

variable "app_role_name" {
  type        = string
  description = "APP role name"
  default     = ""
}

locals {
  aws_account_id = var.aws_account_id == "" ? data.aws_caller_identity.current.account_id : var.aws_account_id
  ec2_role_name  = var.ec2_role_name != "" ? var.ec2_role_name : "aviatrix-role-ec2"
  app_role_name  = var.app_role_name != "" ? var.app_role_name : "aviatrix-role-app"
  aws_partition  = element(split("-", data.aws_region.current.name), 0) == "cn" ? "aws-cn" : "aws"
}

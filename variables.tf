variable "create_iam_roles" {
  type        = bool
  description = "Flag to indicate whether to create IAM roles or not"
  default     = true
}

variable "iam_roles_name_prefix" {
  type        = string
  description = "Name prefix for your EC2 role name and APP role name"
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

variable "external_controller_account_id" {
  type        = string
  description = "External controller account ID"
  default     = ""
}

variable "secondary_account_ids" {
  type        = list(string)
  description = "Secondary account IDs"
  default     = []
}

variable "availability_zone" {
  type        = string
  description = "Availability zone"
  default     = ""
}

variable "vpc_cidr" {
  type        = string
  description = "VPC in which you want launch Aviatrix controller"
  default     = "10.0.0.0/16"
}

variable "subnet_cidr" {
  type        = string
  description = "Subnet in which you want launch Aviatrix controller"
  default     = "10.0.1.0/24"
}

variable "use_existing_vpc" {
  type        = bool
  description = "Flag to indicate whether to use an existing VPC"
  default     = false
}

variable "vpc_id" {
  type        = string
  description = "VPC ID, required when use_existing_vpc is true"
  default     = ""
}

variable "subnet_id" {
  type        = string
  description = "Subnet ID, required when use_existing_vpc is true"
  default     = ""
}

variable "use_existing_keypair" {
  type        = bool
  description = "Flag to indicate whether to use an existing key pair"
  default     = false
}

variable "key_pair_name" {
  type        = string
  description = "Key pair name"
  default     = ""
}

variable "controller_tags" {
  type        = map(string)
  description = "Map of common tags which should be used for module resources"
  default     = {}
}

variable "termination_protection" {
  type        = bool
  description = "Enable/disable switch for termination protection"
  default     = true
}

variable "incoming_ssl_cidrs" {
  type        = list(string)
  description = "CIDRs allowed for HTTPS access"
}

variable "root_volume_size" {
  type        = number
  description = "Root volume size for controller"
  default     = 64
}

variable "root_volume_type" {
  type        = string
  description = "Root volume type for controller"
  default     = "gp2"
}

variable "instance_type" {
  type        = string
  description = "Controller instance size"
  default     = "t3.large"
}

variable "controller_name_prefix" {
  type        = string
  description = "Additional name prefix for your environment resources"
  default     = ""
}

variable "type" {
  type        = string
  description = "Type of billing. Only support 'BYOL'."
  default     = "BYOL"

  validation {
    condition     = contains(["byol"], lower(var.type))
    error_message = "Invalid billing type. Only support 'BYOL'."
  }
}

variable "controller_name" {
  type        = string
  description = "Name of controller that will be launched."
  default     = ""
}

variable "aws_account_id" {
  type        = string
  description = "aws account id"
  default     = ""
}

variable "controller_launch_wait_time" {
  type        = number
  description = "Controller launch wait time"
  default     = 210
}

variable "admin_email" {
  type        = string
  description = "aviatrix controller admin email address"
}

variable "admin_password" {
  type        = string
  description = "aviatrix controller admin password"
#   sensitive = true
}

variable "access_account_email" {
  type        = string
  description = "aviatrix controller access account email"
}

variable "controller_version" {
  type        = string
  description = "The version in which you want launch Aviatrix controller"
  default     = "latest"
}

variable "access_account_name" {
  type        = string
  description = "Access account name"
}

variable "availability_zones" {
  type = list(string)
  default = ["us-east-1a"]
}

variable "customer_license_id" {
  type        = string
  description = "aviatrix customer license id"
  default     = ""
}

locals {
  ec2_role_name = var.create_iam_roles ? module.aviatrix_controller_iam_roles[0].aviatrix_role_ec2_name : var.ec2_role_name
  app_role_name = var.create_iam_roles ? module.aviatrix_controller_iam_roles[0].aviatrix_role_app_name : var.app_role_name
}

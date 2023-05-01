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
  description = "Subnet ID, only required when use_existing_vpc is true"
  default     = ""
}

variable "use_existing_keypair" {
  type        = bool
  default     = false
  description = "Flag to indicate whether to use an existing key pair"
}

variable "key_pair_name" {
  type        = string
  description = "Key pair name"
  default     = ""
}

variable "ec2_role_name" {
  type        = string
  description = "EC2 role for controller"
  default     = ""
}

variable "tags" {
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
  description = "Incoming cidr for security group used by controller"
}

variable "root_volume_size" {
  type        = number
  description = "Root volume disk size for controller"
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

variable "name_prefix" {
  type        = string
  description = "Additional name prefix for your environment resources"
  default     = ""
}

variable "type" {
  default     = "BYOL"
  type        = string
  description = "Type of billing. Only support 'BYOL'."

  validation {
    condition     = contains(["byol"], lower(var.type))
    error_message = "Invalid billing type. Only support 'BYOL'."
  }  
}

variable "controller_name" {
  type        = string
  description = "Name of controller that will be launched. If not set, default name will be used."
  default     = ""
}

data "aws_region" "current" {}

data "aws_availability_zones" "all" {}

data "aws_ec2_instance_type_offering" "offering" {
  for_each = toset(data.aws_availability_zones.all.names)
  
  filter {
    name   = "instance-type"
    values = ["t2.micro", "t3.micro", var.instance_type]
  }

  filter {
    name   = "location"
    values = [each.value]
  }

  location_type = "availability-zone"

  preferred_instance_types = [var.instance_type, "t3.micro", "t2.micro"]
}

locals {
  name_prefix                   = var.name_prefix != "" ? "${var.name_prefix}_" : ""
  controller_name               = var.controller_name != "" ? var.controller_name : "${local.name_prefix}AviatrixController"
  key_pair_name                 = var.key_pair_name != "" ? var.key_pair_name : "controller_kp"
  ec2_role_name                 = var.ec2_role_name != "" ? var.ec2_role_name : "aviatrix-role-ec2"
  is_aws_cn                     = element(split("-", data.aws_region.current.name), 0) == "cn" ? true : false
  images_byol                   = jsondecode(data.http.avx_iam_id.response_body).BYOL
  images_metered                = jsondecode(data.http.avx_iam_id.response_body).Metered
  images_meteredplatinum        = jsondecode(data.http.avx_iam_id.response_body).MeteredPlatinum
  images_meteredplatinumcopilot = jsondecode(data.http.avx_iam_id.response_body).MeteredPlatinumCopilot
  images_vpnmetered             = jsondecode(data.http.avx_iam_id.response_body).VPNMetered
  images_custom                 = jsondecode(data.http.avx_iam_id.response_body).Custom
  ami_id                        = lookup(local.ami_id_map, lower(var.type), null)
  default_az                    = keys({ for az, details in data.aws_ec2_instance_type_offering.offering : az => details.instance_type if details.instance_type == var.instance_type })[0]
  availability_zone             = var.availability_zone != "" ? var.availability_zone : local.default_az

  ami_id_map = {
    byol                   = local.images_byol[data.aws_region.current.name],
    metered                = local.is_aws_cn ? null : local.images_metered[data.aws_region.current.name],
    meteredplatinum        = local.is_aws_cn ? null : local.images_meteredplatinum[data.aws_region.current.name],
    meteredplatinumcopilot = local.is_aws_cn ? null : local.images_meteredplatinumcopilot[data.aws_region.current.name],
    vpnmetered             = local.is_aws_cn ? null : local.images_vpnmetered[data.aws_region.current.name],
    custom                 = local.is_aws_cn ? null : local.images_custom[data.aws_region.current.name],
  }
  common_tags = merge(
    var.tags, {
      module    = "aviatrix-controller-build"
      Createdby = "Terraform+Aviatrix"
  })
}

data "http" "avx_iam_id" {
  url = "https://s3-us-west-2.amazonaws.com/aviatrix-download/AMI_ID/ami_id.json"
  request_headers = {
    "Accept" = "application/json"
  }
}

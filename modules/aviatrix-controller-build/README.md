# Aviatrix - Terraform Modules - Build Controller

## Description

This Terraform module creates an Aviatrix Controller and related components.

## Pre-requisites:

* Accept the terms and subscribe to the Aviatrix Controller in the AWS Marketplace.
Click [here](https://aws.amazon.com/marketplace/pp?sku=zemc6exdso42eps9ki88l9za)
* Aviatrix [IAM roles](../aviatrix-controller-iam-roles)

## Variables

The following variables are required:

| Variable  | Description |
| --------- | ----------- |
| keypair | Key pair name |
| ec2role | EC2 IAM role name |
| incoming_ssl_cidrs | CIDRs allowed for HTTPS access |

The following variables are optional:

| Variable  | Description | Default |
| --------- | ----------- | ------- |
| availability_zone | Availability zone for subnet and controller instance | "" |
| vpc_cidr | VPC where the controller will be launched | "10.0.0.0/16" |
| subnet_cidr | Subnet where the controller will be launched | "10.0.1.0/24" |
| use_existing_vpc | Flag to indicate whether to use an existing VPC | false |
| vpc_id | VPC ID, required when use_existing_vpc is true | "" |
| subnet_id | Subnet ID, only required when use_existing_vpc is true | "" |
| use_existing_keypair | Flag to indicate whether to use an existing key pair | false |
| root_volume_size | The volume size for the controller instance | 64 |
| root_volume_type | The volume type for the controller instance | "gp2" |
| instance_type | The instance type for the controller instance | "t3.large" |
| name_prefix | A prefix to be added to controller resources | "" |
| type | The license type for the Aviatrix controller. Valid values: "Metered", "MeteredPlatinum", "MeteredPlatinumCopilot", "VPNMetered", "BYOL" or "Custom". | "MeteredPlatinumCopilot" |
| controller_name | Controller name | "AviatrixController" |
| termination_protection | Flag to indicate whether termination protection is enabled for the controller | true |
| tags | Map of common tags used for controller resources | {} |

## Outputs

| Variable  | Description |
| --------- | ----------- |
| private_ip | Controller private IP |
| public_ip | Controller public IP |
| vpc_id | VPC ID |
| subnet_id | Subnet ID |
| security_group_id | Security group ID |

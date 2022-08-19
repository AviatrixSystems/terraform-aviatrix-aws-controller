# Launch an Aviatrix Controller in AWS

## Description
This Terraform module allows you to launch an Aviatrix Controller in AWS and create an access account.

## Usage examples

See [examples](https://github.com/AviatrixSystems/terraform-aviatrix-aws-controller/blob/main/examples/README.md)

## Available Submodules

| Module  | Description | Prerequisites |
| ------- | ----------- | ------------- |
| aviatrix-controller-iam-roles | Builds the IAM roles required for controller to connect with this AWS account | None |
| aviatrix-controller-build | Builds the controller | IAM roles created|
| aviatrix-controller-initialize | Initializes the controller (upgrade, set admin email, set admin password, create access account) | Aviatrix Controller |

## Prerequisites

1. [Terraform 0.13](https://www.terraform.io/downloads.html) - execute Terraform scripts
2. [Python3](https://www.python.org/downloads/) - execute Python scripts
3. Create the Python virtual environment and install required dependencies in the terminal
``` shell
 python3 -m venv venv
```
This command will create the virtual environment. In order to use the virtual environment, it needs to be activated by the following command
``` shell
 source venv/bin/activate
```
In order to run Python scripts, dependencies listed in `requirements.txt` need to be installed. For example, the dependencies can be installed by the following command
``` shell
 pip install -r requirements.txt
```

## Variables

The following variables are required:

| Variable  | Description |
| --------- | ----------- |
| incoming_ssl_cidrs | CIDRs allowed for HTTPS access |
| admin_email | Admin email |
| admin_password | Admin password |
| access_account_name | Access account name |
| access_account_email | Access account email |

The following variables are optional:

| Variable  | Description | Default |
| --------- | ----------- | ------- |
| create_iam_roles | Flag to indicate whether to create IAM roles or not | true |
| iam_roles_name_prefix | Name prefix for EC2 role name and APP role name | "" |
| ec2_role_name | EC2 role name | "aviatrix-role-ec2" |
| app_role_name | APP role name | "aviatrix-role-app" |
| external_controller_account_id | External controller account ID | "" |
| secondary_account_ids  | Secondary account IDs | [] |
| availability_zone | Availability zone used for subnet and controller instance | "" |
| use_existing_vpc | Flag to indicate whether to use an existing VPC | false |
| vpc_cidr | VPC where the controller will be launched | "10.0.0.0/16" |
| subnet_cidr | Subnet where the controller will be launched | "10.0.1.0/24" |
| vpc_id | VPC ID, required when use_existing_vpc is true | "" |
| subnet_id | Subnet ID, required when use_existing_vpc is true | "" |
| use_existing_keypair | Flag to indicate whether to use an existing key pair | false |
| key_pair_name | Key pair name | "controller_kp" |
| controller_tags | Map of common tags used for controller resources | {} |
| termination_protection | Flag to indicate whether to enable termination protection | true |
| root_volume_size | Root volume size for controller | 64 |
| root_volume_type | Root volume type for controller | "gp2" |
| instance_type | Controller instance size | "t3.large" |
| controller_name_prefix | Name prefix for controller resources | "" |
| controller_name | Controller name | "AviatrixController" |
| type | Type of billing, can be 'Metered', 'MeteredPlatinum', 'MeteredPlatinumCopilot', 'VPNMetered', BYOL' or 'Custom' | "MeteredPlatinumCopilot" |
| aws_account_id | The AWS account ID | Current caller ID |
| controller_launch_wait_time | Controller launch wait time | 210 |
| controller_version | Controller version | "latest" |
| customer_license_id | Customer license ID | "" |
| private_mode | Flag to enable private_mode. Requires usage of existing VPC with connectivity | false |

## Outputs

| Variable  | Description |
| --------- | ----------- |
| public_ip | Controller public IP |
| private_ip | Controller private IP |
| vpc_id | VPC where Aviatrix controller was built |
| subnet_id | Subnet where Aviatrix controller was built |
| security_group_id | Controller security group ID |

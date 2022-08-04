## Launch an Aviatrix Controller in AWS

### Description
This Terraform module allows you to launch an Aviatrix Controller in AWS and create an access account.

### Procedures for Building and Initializing a Controller in AWS

#### 1. Install required dependencies

Install required dependencies.

``` shell
 pip install -r requirements.txt
```

#### 2. Applying Terraform configuration

Build and initialize the Aviatrix Controller

```hcl
module "aviatrix_controller_aws" {
  source               = "AviatrixSystems/aws-controller/aviatrix"
  keypair              = "<<< KEY PAIR NAME >>>"
  incoming_ssl_cidrs   = ["<<< TRUSTED MANAGEMENT CIDR 1 >>>", ...]
  admin_password       = "<<< ADMIN PASSWORD >>>"
  admin_email          = "<<< ADMIN EMAIL >>>"
  access_account_name  = "<<< ACCESS ACCOUNT NAME >>>"
  access_account_email = "<<< ACCESS ACCOUNT EMAIL >>>"
  customer_license_id  = "<<< CUSTOMER LICENSE ID >>>"
}

output "public_ip" {
  value = module.aviatrix_controller_aws.public_ip
}

output "private_ip" {
  value = module.aviatrix_controller_aws.private_ip
}
```

*Execute*

```shell
terraform init
terraform apply
```

### Variables

The following variables are required:

| Variable  | Description |
| --------- | ----------- |
| keypair | Key pair name |
| incoming_ssl_cidrs | CIDRs allowed for HTTPS access |
| admin_email | Admin email |
| admin_password | Admin password |
| access_account_name | Access account name |
| access_account_email | Access account email |

The following variables are optional:

| Variable  | Description | Default |
| --------- | ----------- | ------- |
| create_iam_roles | Flag to indicate whether to create IAM roles or not | true |
| iam_roles_tags | Map of common tags used for IAM roles | {} |
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
| controller_tags | Map of common tags used for controller resources | {} |
| termination_protection | Flag to indicate whether to enable termination protection | true |
| root_volume_size | Root volume size for controller | 64 |
| root_volume_type | Root volume type for controller | "gp2" |
| instance_type | Controller instance size | "t3.large" |
| controller_name_prefix | Name prefix for controller resources | "" |
| type | Type of billing, can be 'Metered', 'MeteredPlatinum', 'MeteredPlatinumCopilot', 'VPNMetered', BYOL' or 'Custom' | "MeteredPlatinumCopilot" |
| controller_name | Controller name | "AviatrixController" |
| controller_launch_wait_time | Controller launch wait time | 210 |
| controller_version | Controller version | "latest" |
| customer_license_id | Customer license ID | "" |

### Outputs

| Variable  | Description |
| --------- | ----------- |
| public_ip | Controller public IP |
| private_ip | Controller private IP |
| vpc_id | VPC where Aviatrix controller was built |
| subnet_id | Subnet where Aviatrix controller was built |
| security_group_id | Controller security group ID |

### Available Modules

| Module  | Description | Prerequisites |
| ------- | ----------- | ------------- |
| [aviatrix-controller-iam-roles](./modules/aviatrix-controller-iam-roles) | Builds the IAM roles required for Aviatrix to connect with this AWS account | None |
| [aviatrix-controller-build](./modules/aviatrix-controller-build) | Builds the controller | IAM roles created|
| [aviatrix-controller-initialize](./modules/aviatrix-controller-initialize) | Initializes the Controller (Upgrade, set admin e-mail, set admin password, create access account) | Aviatrix Controller |

# Usage Examples

This document contains examples of different use cases. For full details on available variables, please see the README of each module.

## 1. Creating IAM roles, launching and initializing a controller

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

## 2. Launching and initializing a controller without creating IAM roles

> **NOTE:** IAM roles are still required for building the controller. In the following example, default EC2 role name
> APP role name are used.

```hcl
module "aviatrix_controller_aws" {
  source               = "AviatrixSystems/aws-controller/aviatrix"
  create_iam_roles     = false
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

## 3. Creating IAM roles, launching and initializing a controller in an existing VPC

> **NOTE:** In the first step of destroying a controller, a controller API will be called to delete the security groups
> added during the initialization. If the controller loses the internet access before the API call, the security groups
> won't be properly deleted. Therefore, please make sure the resources on which the internet access depends will be
> destroyed after the security groups are deleted. 

```hcl
module "aviatrix_controller_aws" {
  source               = "AviatrixSystems/aws-controller/aviatrix"
  keypair              = "<<< KEY PAIR NAME >>>"
  use_existing_vpc     = true
  vpc_id               = "<<< VPC ID >>>"
  subnet_id            = "<<< SUBNET ID>>>"
  incoming_ssl_cidrs   = ["<<< TRUSTED MANAGEMENT CIDR 1 >>>", ...]
  admin_password       = "<<< ADMIN PASSWORD >>>"
  admin_email          = "<<< ADMIN EMAIL >>>"
  access_account_name  = "<<< ACCESS ACCOUNT NAME >>>"
  access_account_email = "<<< ACCESS ACCOUNT EMAIL >>>"
  customer_license_id  = "<<< CUSTOMER LICENSE ID >>>"
  
  # For example, Terraform resources, such as internet gateway, route table, route, route table association, etc., can 
  # be put in "depends_on", if used.
  depends_on = []
}

output "public_ip" {
  value = module.aviatrix_controller_aws.public_ip
}

output "private_ip" {
  value = module.aviatrix_controller_aws.private_ip
}
```

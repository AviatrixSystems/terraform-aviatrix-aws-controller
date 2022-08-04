## Aviatrix - Terraform Modules - Build Controller

### Description

This Terraform module creates an Aviatrix Controller and related components in an existing AWS environment.

### Pre-requisites:

* Accept the terms and subscribe to the Aviatrix Controller in the AWS Marketplace.
Click [here](https://aws.amazon.com/marketplace/pp?sku=zemc6exdso42eps9ki88l9za)
* Aviatrix [IAM roles](../aviatrix-controller-iam-roles)

### Variables

- **availability_zone**

  Availability zone for subnet and controller instance. Default value: "".

- **vpc_cidr**

  VPC in which you want launch Aviatrix controller. Default value: "10.0.0.0/16".

- **subnet_cidr**

  Subnet in which you want launch Aviatrix controller. Default value: "10.0.1.0/24".

- **use_existing_vpc**

  Flag to indicate whether to use an existing VPC. Default value: false.

- **vpc_id**

  VPC ID, required when use_existing_vpc is true. Default value: "".

- **subnet_id**

  Subnet ID, only required when use_existing_vpc is true. Default: "".

- **use_existing_keypair**

  Flag to indicate whether to use an existing key pair. Default: false.

- **keypair**

  The name of the AWS Key Pair.
  
- **ec2role**

  The name of the EC2 IAM role.

- **incoming_ssl_cidrs**

  The CIDRs to be allowed for HTTPS(port 443) access to the controller. Type is "list".

- **tags** 

  Additional map of tags passed to mark resources create by module. Default value: {}.
  
- **termination_protection**

  Whether termination protection is enabled for the controller. Default value: true.
  
- **root_volume_size**
  
  The size of the hard disk for the controller instance. Default value: 64.

- **root_volume_type**
  
  The type of the hard disk for the controller instance, Default value: "gp2".

- **instance_type**

  The instance size for the Aviatrix controller instance. Default value: "t3.large".

- **name_prefix**

  A prefix to be added to the Aviatrix controller instance name. Default value: "".

- **type**

  The license type for the Aviatrix controller. Valid values: "Metered", "MeteredPlatinum", "MeteredPlatinumCopilot", 
  "VPNMetered", "BYOL" or "Custom". Default value: "MeteredPlatinumCopilot". 
  
- **controller_name**
  
  Name of controller that will be launched. Default: "AviatrixController".

### Outputs

- **private_ip**

  The private IP address of the AWS EC2 instance created for the controller.

- **public_ip**

  The public IP address of the AWS EC2 instance created for the controller.

- **vpc_id**

  VPC ID.

- **subnet_id**

  Subnet ID.

- **security_group_id**

  Security group ID.

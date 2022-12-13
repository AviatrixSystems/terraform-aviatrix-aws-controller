# Aviatrix - Terraform Modules - Initialize Controller

## Description

This Terraform module initializes a newly created Aviatrix Controller by running local Python code.

> **NOTE:** In the first step of destroying a controller, a controller API will be called to delete the security groups 
> added during the initialization. If the controller loses the internet access before the API call, the security groups 
> won't be properly deleted. Therefore, please make sure the resources on which the internet access depends will be 
> destroyed after the security groups are deleted. For example, please properly fill "depends_on" with resources and 
> modules, such as internet gateway, route table, route, route table association, aviatrix-controller-build, etc.

## Variables

The following variables are required:

| Variable  | Description |
| --------- | ----------- |
| public_ip | The Controller's public IP address |
| private_ip | The Controller's private IP address |
| admin_email | The administrator's email address |
| admin_password | The administrator's password |
| access_account_name | Access account name |
| access_account_email | Access account email |

The following variables are optional:

| Variable  | Description | Default |
| --------- | ----------- | ------- |
| aws_account_id | The AWS account ID | Current caller ID |
| controller_launch_wait_time | Time in second to wait for controller to be up | 210 |
| customer_license_id |The customer license ID. Required if using a BYOL controller.| "" |
| controller_version | The controller version | "latest" |
| ec2_role_name | EC2 role name | "aviatrix-role-ec2" |
| app_role_name | APP role name | "aviatrix-role-app" |
| controller_display_name | Controller name displayed in UI.| "" |
| controller_time_zone | Controller time zone.| "" |

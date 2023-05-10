# Aviatrix - Terraform Modules - Create IAM Roles

## Description
This Terraform module creates AWS IAM credentials (IAM roles, policies, etc...), which are used to grant AWS API
permissions for Aviatrix controller in order to allow the controller to access resources in AWS account(s). This
Terraform module should be run in the AWS account where you are installing the Controller and any additional AWS 
accounts that will be connected to the Controller.

If this module is applied for setting up IAM credentials on the AWS account where your controller is (going to be)
located, the Terraform variable, "external_controller_account_id" should NOT be set.

If this module is applied for AWS account(s), which will be managed by the controller, please configure the Terraform
variable, "external_controller_account_id" and set the value to be the AWS account ID of the controller.

Please refer to the documentation below for more detail:
[documentation](https://docs.aviatrix.com/HowTos/HowTo_IAM_role.html).

## Variables

The following variables are optional:

> **NOTE:** If customized **ec2_role_name** and **app_role_name** are used, **name_prefix** will be ignored.

| Variable                       | Description                                                                                                                                                                                                                                                                                                             | Default             |
|--------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------|
| name_prefix                    | A prefix to be added to the default role names                                                                                                                                                                                                                                                                          | ""                  |
| ec2_role_name                  | EC2 role name                                                                                                                                                                                                                                                                                                           | "aviatrix-role-ec2" |
| app_role_name                  | APP role name                                                                                                                                                                                                                                                                                                           | "aviatrix-role-app" |
| secondary_account_ids          | A list of secondary AWS account IDs. ONLY use this parameter if this Terraform module is applied on the AWS account of your controller                                                                                                                                                                                  | []                  |
| external_controller_account_id | The AWS account ID where the Aviatrix Controller was/will be launched. This is only required if you are creating roles for the secondary account different from the account where controller was/will be launched. DO NOT use this parameter if this Terraform module is applied on the AWS account of your controller. | ""                  |

## Outputs
| Variable                        | Description                                   |
|---------------------------------|-----------------------------------------------|
| aws_account_id                  | AWS account ID                                |
| aviatrix_role_ec2_name          | Aviatrix role name for EC2                    |
| aviatrix_role_ec2_arn           | Aviatrix role ARN for EC2                     |
| aviatrix_role_app_name          | Aviatrix role name for application            |
| aviatrix_role_app_arn           | Aviatrix role ARN for application             |
| aviatrix_assume_role_policy_arn | Aviatrix assume role policy ARN               |
| aviatrix_app_policy_arn         | Aviatrix policy ARN for application           |
| aviatrix_role_ec2_profile_arn   | Aviatrix role EC2 profile ARN for application |

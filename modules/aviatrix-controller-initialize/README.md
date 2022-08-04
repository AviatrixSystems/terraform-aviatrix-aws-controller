## Aviatrix - Terraform Modules - Initialize Controller

### Description

This Terraform module initializes a newly created Aviatrix Controller by running local Python code.

> **NOTE:** Please properly fill "depends_on" with resources and modules, such as internet gateway, route table, route,
> route table association, aviatrix-controller-build, etc. When destroying the controller, a controller API will be
> called to clean up the security groups. If the controller lost the internet access before the API call, the destroy
> process would hang.

### Variables

- **admin_email**

  The administrator's email address. This email address will be used for password recovery as well as for notifications
  from the Controller.

- **admin_password**

  The administrator's password. The default password is the Controller's private IP addresses. It will be changed to this
  value as part of the initialization.

- **private_ip**

  The Controller's private IP address.

- **public_ip**

  The Controller's public IP address.

- **access_account_name**

  Access account name.

- **access_account_email**

  Access account email.

- **aws_account_id**

  The AWS account ID.

- **customer_license_id**

  The customer license ID, optional. Required if using a BYOL controller.
  
- **controller_version**
  
  The version to which you want to initialize the Aviatrix controller.
    
- **controller_launch_wait_time**
 
  Time in second to wait for controller to be up. Default value: 210.

- **ec2_role_name**

  EC2 role name. Default value: "aviatrix-role-ec2".

- **app_role_name**

  APP role name. Default value: "aviatrix-role-app".

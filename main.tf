module "aviatrix_controller_iam_roles" {
  count                          = var.create_iam_roles ? 1 : 0
  source                         = "./modules/aviatrix-controller-iam-roles"
  name_prefix                    = var.iam_roles_name_prefix
  ec2_role_name                  = var.ec2_role_name
  app_role_name                  = var.app_role_name
  external_controller_account_id = var.external_controller_account_id
  secondary_account_ids          = var.secondary_account_ids
}

module "aviatrix_controller_build" {
  source                 = "./modules/aviatrix-controller-build"
  availability_zone      = var.availability_zone
  vpc_cidr               = var.vpc_cidr
  subnet_cidr            = var.subnet_cidr
  use_existing_vpc       = var.use_existing_vpc
  vpc_id                 = var.vpc_id
  subnet_id              = var.subnet_id
  use_existing_keypair   = var.use_existing_keypair
  key_pair_name          = var.key_pair_name
  ec2_role_name          = local.ec2_role_name
  name_prefix            = var.controller_name_prefix
  controller_name        = var.controller_name
  type                   = var.type
  root_volume_size       = var.root_volume_size
  root_volume_type       = var.root_volume_type
  instance_type          = var.instance_type
  termination_protection = var.termination_protection
  incoming_ssl_cidrs     = var.incoming_ssl_cidrs
  tags                   = var.controller_tags
}

data "aws_caller_identity" "current" {}

module "aviatrix_controller_initialize" {
  source                      = "./modules/aviatrix-controller-initialize"
  aws_account_id              = var.aws_account_id == "" ? data.aws_caller_identity.current.account_id : var.aws_account_id
  controller_launch_wait_time = var.controller_launch_wait_time
  public_ip                   = module.aviatrix_controller_build.public_ip
  private_ip                  = module.aviatrix_controller_build.private_ip
  admin_email                 = var.admin_email
  admin_password              = var.admin_password
  access_account_email        = var.access_account_name
  access_account_name         = var.access_account_name
  customer_license_id         = var.customer_license_id
  controller_version          = var.controller_version
  ec2_role_name               = local.ec2_role_name
  app_role_name               = local.app_role_name
  controller_display_name     = var.controller_display_name
  controller_time_zone        = var.controller_time_zone

  depends_on = [
    module.aviatrix_controller_build
  ]
}

locals {
  argument_create = format("'%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s'",
    var.controller_launch_wait_time, local.aws_account_id, var.public_ip, var.private_ip, var.admin_email,
    var.admin_password, var.access_account_email, var.controller_version, var.access_account_name,
  var.customer_license_id, local.ec2_role_name, local.app_role_name, local.aws_partition, var.private_mode)

  argument_destroy = format("'%s' '%s'",
    local.controller_ip, var.admin_password
  )

  controller_ip = var.private_mode ? var.private_ip : var.public_ip
}

resource "null_resource" "run_script" {
  triggers = {
    argument_destroy = local.argument_destroy
  }

  provisioner "local-exec" {
    command = "python3 -W ignore ${path.module}/aviatrix_controller_init.py ${local.argument_create}"
  }

  provisioner "local-exec" {
    when       = destroy
    command    = "python3 -W ignore ${path.module}/disable_controller_sg_mgmt.py ${self.triggers.argument_destroy}"
    on_failure = continue
  }
}

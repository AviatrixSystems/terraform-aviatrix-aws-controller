import logging
import sys
from aviatrix_controller_init import send_aviatrix_api, login, verify_aviatrix_api_response_login


class AviatrixException(Exception):
    def __init__(self, message="Aviatrix Error Message: ..."):
        super(AviatrixException, self).__init__(message)


def disable_controller_sg_mgmt(
        api_endpoint_url,
        CID
):
    data = {
        "action": "disable_controller_security_group_management",
        "CID": CID
    }

    response = send_aviatrix_api(
        api_endpoint_url=api_endpoint_url,
        request_method="POST",
        payload=data,
        timeout=60
    )

    return response


def function_handler(event):
    public_ip = event["public_ip"]
    admin_password = event["admin_password"]

    api_endpoint_url = (
            "https://" + public_ip + "/v1/api"
    )

    logging.info("CLEANING UP START: Disable the controller security group management.")

    response = login(
        api_endpoint_url=api_endpoint_url,
        username="admin",
        password=admin_password,
    )

    verify_aviatrix_api_response_login(response=response)
    CID = response.json()["CID"]

    response = disable_controller_sg_mgmt(
        api_endpoint_url=api_endpoint_url,
        CID=CID
    )

    py_dict = response.json()

    response_code = response.status_code
    if response_code != 200:
        err_msg = (
                "Fail to disable controller security group management. The response code is" + response_code
        )
        raise AviatrixException(message=err_msg)

    api_return_boolean = py_dict["return"]
    if api_return_boolean is not True:
        err_msg = "Fail to disable controller security group management. The Response is" + str(py_dict)
        raise AviatrixException(
            message=err_msg,
        )

    logging.info("CLEANING UP ENDED: Disabled the controller security group management.")


if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s disable-controller-sg-mgmt--- %(message)s", level=logging.INFO
    )

    i = 1
    public_ip = sys.argv[i]
    i += 1
    admin_password = sys.argv[i]

    event = {
        "public_ip": public_ip,
        "admin_password": admin_password
    }

    try:
        function_handler(event)
    except Exception as e:
        logging.exception("")
    else:
        logging.info("Controller security group management has been disabled.")

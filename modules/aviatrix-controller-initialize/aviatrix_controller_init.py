import json
import logging
import sys
import time
import traceback
import requests

# The wait time from experience is between 60 to 600 seconds
default_wait_time_for_apache_wakeup = 600


class AviatrixException(Exception):
    def __init__(self, message="Aviatrix Error Message: ..."):
        super(AviatrixException, self).__init__(message)


# END class MyException


def function_handler(event):
    public_ip = event["public_ip"]
    aviatrix_api_version = event["aviatrix_api_version"]
    aviatrix_api_route = event["aviatrix_api_route"]
    private_ip = event["private_ip"]
    admin_email = event["admin_email"]
    new_admin_password = event["new_admin_password"]
    access_account_email = event["account_email"]
    access_account_name = event["access_account_name"]
    customer_license_id = event["customer_license_id"]
    controller_init_version = event["controller_init_version"]
    controller_launch_wait_time = event["controller_launch_wait_time"]

    # Reconstruct some parameters
    customer_license_id = customer_license_id.rstrip()
    customer_license_id = customer_license_id.lstrip()
    api_endpoint_url = (
            "https://" + public_ip + "/" + aviatrix_api_version + "/" + aviatrix_api_route
    )

    # Step1. Wait until the rest API service of Aviatrix Controller is up and running
    logging.info(
        "START: Sleep for %s seconds, waiting for instance to be up", controller_launch_wait_time
    )

    time.sleep(controller_launch_wait_time)
    wait_until_controller_api_server_is_ready(
        hostname=public_ip,
        api_version=aviatrix_api_version,
        api_route=aviatrix_api_route,
        total_wait_time=controller_launch_wait_time,
        interval_wait_time=10,
    )
    logging.info("ENDED: Sleep")

    # Step2. Login Aviatrix Controller with username: Admin and password: private ip address and verify login
    logging.info("START: Login Aviatrix Controller as admin using private ip address")
    response = login(
        api_endpoint_url=api_endpoint_url,
        username="admin",
        password=private_ip,
        hide_password=False,
    )

    verify_aviatrix_api_response_login(response=response)
    CID = response.json()["CID"]
    logging.info("END: Login Aviatrix Controller as admin using private ip address")

    # Step3. Check if the controller has been initialized or not
    logging.info("START: Check if Aviatrix Controller has already been initialized")
    is_controller_initialized = has_controller_initialized(
        api_endpoint_url=api_endpoint_url,
        CID=CID,
    )

    if is_controller_initialized:
        err_msg = "ERROR: Controller has already been initialized"
        logging.error(err_msg)
        raise AviatrixException(message=err_msg)

    logging.info("END: Check if Aviatrix Controller has already been initialized")

    # Step4. Set admin email
    logging.info("Start: Set admin email")
    response = set_admin_email(
        api_endpoint_url=api_endpoint_url,
        CID=CID,
        admin_email=admin_email,
    )

    verify_aviatrix_api_set_admin_email(response=response)
    logging.info("End: Set admin email")

    # Step5. set admin password
    logging.info("Start: Set admin password")
    response = set_admin_password(
        api_endpoint_url=api_endpoint_url,
        CID=CID,
        old_admin_password=private_ip,
        new_admin_password=new_admin_password,
    )

    verify_aviatrix_api_set_admin_password(response=response)
    logging.info("End: Set admin password")

    # Step6. Login Aviatrix Controller as admin with new password
    logging.info("Start: Login in as admin with new password")
    response = login(
        api_endpoint_url=api_endpoint_url,
        username="admin",
        password=new_admin_password,
    )

    CID = response.json()["CID"]
    verify_aviatrix_api_set_admin_password(response=response)
    logging.info("End: Login as admin with new password")

    # Step7. Initial Setup for Aviatrix Controller by Invoking Aviatrix API
    logging.info("Start: Aviatrix Controller initial setup")
    response = run_initial_setup(
        api_endpoint_url=api_endpoint_url,
        CID=CID,
        target_version=controller_init_version,
    )
    verify_aviatrix_api_run_initial_setup(response=response)
    logging.info("End: Aviatrix Controller initial setup")

    time.sleep(20)

    # Step8. Wait until apache server of controller is up and running after initial setup
    logging.info(
        "START: Wait until API server of Aviatrix Controller is up and running after initial setup"
    )
    wait_until_controller_api_server_is_ready(
        hostname=public_ip,
        api_version=aviatrix_api_version,
        api_route=aviatrix_api_route,
        total_wait_time=default_wait_time_for_apache_wakeup,
        interval_wait_time=10,
    )
    logging.info(
        "End: Wait until API server of Aviatrix Controller is up ans running after initial setup"
    )

    # Step9. Re-login
    logging.info("START: Re-login")
    response = login(
        api_endpoint_url=api_endpoint_url,
        username="admin",
        password=new_admin_password,
    )
    verify_aviatrix_api_response_login(response=response)
    CID = response.json()["CID"]
    logging.info("END: Re-login")

    # Step10. Set Aviatrix Customer ID
    logging.info("START: Set Aviatrix Customer ID by invoking aviatrix API")
    response = set_aviatrix_customer_id(
        api_endpoint_url=api_endpoint_url,
        CID=CID,
        customer_id=customer_license_id,
    )
    py_dict = response.json()
    logging.info("Aviatrix API response is : " + str(py_dict))
    logging.info("END: Set Aviatrix Customer ID by invoking aviatrix API")

    # Step11. Create Access Account
    logging.info("START : Create the Access Accounts")

    controller_region = event["controller_region"]
    ec2_role_name = event["ec2_role_name"]
    app_role_name = event["app_role_name"]

    app_role_arn = "arn:" + controller_region + ":iam::{AWS_ACCOUNT_ID}:role/" + app_role_name
    app_role_arn = app_role_arn.format(AWS_ACCOUNT_ID=aws_account_id)
    ec2_role_arn = "arn:" + controller_region + ":iam::{AWS_ACCOUNT_ID}:role/" + ec2_role_name
    ec2_role_arn = ec2_role_arn.format(AWS_ACCOUNT_ID=aws_account_id)
    if controller_region == "aws":
        cloud_type = "1"
    elif controller_region == "aws-cn":
        cloud_type = "1024"

    response = create_access_account(
        api_endpoint_url=api_endpoint_url,
        CID=CID,
        account_name=access_account_name,
        account_email=access_account_email,
        cloud_type=cloud_type,
        aws_account_number=aws_account_id,
        is_iam_role_based="true",
        app_role_arn=app_role_arn,
        ec2_role_arn=ec2_role_arn,
    )

    verify_aviatrix_api_create_access_account(
        response=response,
        admin_email=admin_email,
    )

    logging.info("END : Create the Access Account")


def wait_until_controller_api_server_is_ready(
        hostname="123.123.123.123",
        api_version="v1",
        api_route="api",
        total_wait_time=300,
        interval_wait_time=10,
):
    api_endpoint_url = "https://" + hostname + "/" + api_version + "/" + api_route

    # invoke the aviatrix api with a non-existed api
    # to resolve the issue where server status code is 200 but response message is "Valid action required: login"
    # which means backend is not ready yet
    payload = {"action": "login", "username": "test", "password": "test"}
    remaining_wait_time = total_wait_time

    """ Variable Description: (time_spent_for_requests_lib_timeout)
    Description: 
        * This value represents how many seconds for "requests" lib to timeout by default. 
    Detail: 
        * The value 20 seconds is actually a rough number  
        * If there is a connection error and causing timeout when 
          invoking--> requests.get(xxx), it takes about 20 seconds for requests.get(xxx) to throw timeout exception.
        * When calculating the remaining wait time, this value is considered.
    """
    time_spent_for_requests_lib_timeout = 20
    last_err_msg = ""
    while remaining_wait_time > 0:
        try:
            # Reset the checking flags
            response_status_code = -1
            is_apache_returned_200 = False
            is_api_service_ready = False

            # invoke a dummy REST API to Aviatrix controller
            response = requests.post(url=api_endpoint_url, data=payload, verify=False)

            # check response
            # if the server is ready, the response code should be 200.
            # there are two cases that the response code is 200
            #   case1 : return value is false and the reason message is "Valid action required: login",
            #           which means the server is not ready yet
            #   case2 : return value is false and the reason message is "username ans password do not match",
            #           which means the server is ready
            if response is not None:
                response_status_code = response.status_code
                logging.info("Server status code is: %s", str(response_status_code))
                py_dict = response.json()
                if response.status_code == 200:
                    is_apache_returned_200 = True

                response_message = py_dict["reason"]
                response_msg_indicates_backend_not_ready = "Valid action required"
                # case1:
                if (
                        py_dict["return"] is False
                        and response_msg_indicates_backend_not_ready in response_message
                ):
                    is_api_service_ready = False
                    logging.info(
                        "Server is not ready, and the response is :(%s)",
                        response_message,
                    )
                # case2:
                else:
                    is_api_service_ready = True
            # END outer if

            # if the response code is 200 and the server is ready
            if is_apache_returned_200 and is_api_service_ready:
                logging.info("Server is ready")
                return True
        except Exception as e:
            logging.exception(
                "Aviatrix Controller %s is not available", api_endpoint_url
            )
            last_err_msg = str(e)
            pass
            # END try-except

        # handle the response code is 404
        if response_status_code == 404:
            err_msg = (
                    "Error: Aviatrix Controller returns error code: 404 for "
                    + api_endpoint_url
            )
            raise AviatrixException(
                message=err_msg,
            )
        # END if

        # if server response code is neither 200 nor 404, some other errors occurs
        # repeat the process till reaches case 2

        remaining_wait_time = (
                remaining_wait_time
                - interval_wait_time
                - time_spent_for_requests_lib_timeout
        )
        if remaining_wait_time > 0:
            time.sleep(interval_wait_time)
    # END while loop

    # if the server is still not ready after the default time
    # raise AviatrixException
    err_msg = (
            "Aviatrix Controller "
            + api_endpoint_url
            + " is not available after "
            + str(total_wait_time)
            + " seconds"
            + "Server status code is: "
            + str(response_status_code)
            + ". "
            + "The response message is: "
            + last_err_msg
    )
    raise AviatrixException(
        message=err_msg,
    )


# END wait_until_controller_api_server_is_ready()


def login(
        api_endpoint_url="https://123.123.123.123/v1/api",
        username="admin",
        password="********",
        hide_password=True,
):
    request_method = "POST"
    data = {"action": "login", "username": username, "password": password}
    logging.info("API endpoint url is : %s", api_endpoint_url)
    logging.info("Request method is : %s", request_method)

    # handle if the hide_password is selected
    if hide_password:
        payload_with_hidden_password = dict(data)
        payload_with_hidden_password["password"] = "************"
        logging.info(
            "Request payload: %s",
            str(json.dumps(obj=payload_with_hidden_password, indent=4)),
        )
    else:
        logging.info("Request payload: %s", str(json.dumps(obj=data, indent=4)))

    # send post request to the api endpoint
    response = send_aviatrix_api(
        api_endpoint_url=api_endpoint_url,
        request_method=request_method,
        payload=data,
    )
    return response


# End def login()


def send_aviatrix_api(
        api_endpoint_url="https://123.123.123.123/v1/api",
        request_method="POST",
        payload=dict(),
        retry_count=5,
        timeout=None,
):
    response = None
    responses = list()
    request_type = request_method.upper()
    response_status_code = -1

    for i in range(retry_count):
        try:
            if request_type == "GET":
                response = requests.get(
                    url=api_endpoint_url, params=payload, verify=False
                )
                response_status_code = response.status_code
            elif request_type == "POST":
                response = requests.post(
                    url=api_endpoint_url, data=payload, verify=False, timeout=timeout
                )
                response_status_code = response.status_code
            else:
                failure_reason = "ERROR : Bad HTTPS request type: " + request_type
                logging.error(failure_reason)
        except requests.exceptions.Timeout as e:
            logging.exception("WARNING: Request timeout...")
            responses.append(str(e))
        except requests.exceptions.ConnectionError as e:
            logging.exception("WARNING: Server is not responding...")
            responses.append(str(e))
        except Exception as e:
            traceback_msg = traceback.format_exc()
            logging.exception("HTTP request failed")
            responses.append(str(traceback_msg))
            # For error message/debugging purposes

        finally:
            if response_status_code == 200:
                return response
            elif response_status_code == 404:
                failure_reason = "ERROR: 404 Not Found"
                logging.error(failure_reason)

            # if the response code is neither 200 nor 404, repeat the precess (retry)
            # the default retry count is 5, the wait for each retry is i
            # i           =  0  1  2  3  4
            # wait time   =     1  2  4  8

            if i + 1 < retry_count:
                logging.info("START: retry")
                logging.info("i == %d", i)
                wait_time_before_retry = pow(2, i)
                logging.info("Wait for: %ds for the next retry", wait_time_before_retry)
                time.sleep(wait_time_before_retry)
                logging.info("ENDED: Wait until retry")
                # continue next iteration
            else:
                failure_reason = (
                        "ERROR: Failed to invoke Aviatrix API. Exceed the max retry times. "
                        + " All responses are listed as follows :  "
                        + str(responses)
                )
                raise AviatrixException(
                    message=failure_reason,
                )
            # END
    return response


# End def send_aviatrix_api()


def verify_aviatrix_api_response_login(response=None):
    # if successfully login
    # response_code == 200
    # api_return_boolean == true
    # response_message = "authorized successfully"

    py_dict = response.json()
    logging.info("Aviatrix API response is %s", str(py_dict))

    response_code = response.status_code
    if response_code != 200:
        err_msg = (
                "Fail to login Aviatrix Controller. The response code is" + response_code
        )
        raise AviatrixException(message=err_msg)

    api_return_boolean = py_dict["return"]
    if api_return_boolean is not True:
        err_msg = "Fail to Login Aviatrix Controller. The Response is" + str(py_dict)
        raise AviatrixException(
            message=err_msg,
        )

    api_return_msg = py_dict["results"]
    expected_string = "authorized successfully"
    if (expected_string in api_return_msg) is not True:
        err_msg = "Fail to Login Aviatrix Controller. The Response is" + str(py_dict)
        raise AviatrixException(
            message=err_msg,
        )


# End def verify_aviatrix_api_response_login()


def has_controller_initialized(
        api_endpoint_url="123.123.123.123/v1/api",
        CID="ABCD1234",
):
    request_method = "GET"
    data = {"action": "initial_setup", "subaction": "check", "CID": CID}
    logging.info("API endpoint url: %s", str(api_endpoint_url))
    logging.info("Request method is: %s", str(request_method))
    logging.info("Request payload is : %s", str(json.dumps(obj=data, indent=4)))

    response = send_aviatrix_api(
        api_endpoint_url=api_endpoint_url,
        request_method=request_method,
        payload=data,
    )

    py_dict = response.json()
    logging.info("Aviatrix API response is: %s", str(py_dict))

    if py_dict["return"] is False and "not run" in py_dict["reason"]:
        return False
    else:
        return True


# End def has_controller_initialized()


def set_admin_email(
        api_endpoint_url="123.123.123.123/v1/api",
        CID="ABCD1234",
        admin_email="avx@aviatrix.com",
):
    request_method = "POST"
    data = {"action": "add_admin_email_addr", "CID": CID, "admin_email": admin_email}

    logging.info("API endpoint url: %s", str(api_endpoint_url))
    logging.info("Request method is: %s", str(request_method))
    logging.info("Request payload is : %s", str(json.dumps(obj=data, indent=4)))

    response = send_aviatrix_api(
        api_endpoint_url=api_endpoint_url,
        request_method=request_method,
        payload=data,
    )
    return response


# End def set_admin_email()


def verify_aviatrix_api_set_admin_email(response=None):
    # if the set admin email request is successful
    # the response code is 200 and the returned message is "admin email address has been successfully added"
    py_dict = response.json()
    logging.info("Aviatrix API response is %s", str(py_dict))

    response_code = response.status_code
    if response_code != 200:
        err_msg = (
                "Fail for set admin email for the Aviatrix Controller. The response code is"
                + response_code
        )
        raise AviatrixException(message=err_msg)

    api_return_message = py_dict["results"]
    expected_string = "admin email address has been successfully added"
    if (expected_string in api_return_message) is False:
        err_msg = (
                "Fail for set admin email for Aviatrix Controller. The expected string "
                + expected_string
                + " is not found in returned message"
        )
        raise AviatrixException(message=err_msg)


# End def verify_aviatrix_api_set_admin_email()


def set_admin_password(
        api_endpoint_url="123.123.123.123/v1/api",
        CID="ABCD1234",
        old_admin_password="********",
        new_admin_password="********",
):
    # The api name changes from "change_password" to "edit_account_user"
    request_method = "POST"
    data_1st_try = {
        "action": "edit_account_user",
        "CID": CID,
        "username": "admin",
        "what": "password",
        "old_password": old_admin_password,
        "new_password": new_admin_password,
    }
    payload_with_hidden_password = dict(data_1st_try)
    payload_with_hidden_password["new_password"] = "********"

    logging.info("API endpoint url: %s", str(api_endpoint_url))
    logging.info("Request method is: %s", str(request_method))
    logging.info(
        "Request payload is : %s",
        str(json.dumps(obj=payload_with_hidden_password, indent=4)),
    )

    response = send_aviatrix_api(
        api_endpoint_url=api_endpoint_url,
        request_method=request_method,
        payload=data_1st_try,
    )

    # if response return false the "Valid action required"
    # the api doesn't exist
    if (
            response.json()["return"] == False
            and "Valid action required" in response.json()["reason"]
    ):
        is_successfully_changed_password = False
    else:
        return response

    # if the api doesn't exist, try the "change_password" api
    data_2nd_try = {
        "action": "change_password",
        "CID": CID,
        "account_name": "admin",
        "username": "admin",
        "old_password": old_admin_password,
        "password": new_admin_password,
    }
    payload_with_hidden_password = dict(data_2nd_try)
    payload_with_hidden_password["password"] = "********"

    logging.info("API endpoint url: %s", str(api_endpoint_url))
    logging.info("Request method is: %s", str(request_method))
    logging.info(
        "Request payload is : %s",
        str(json.dumps(obj=payload_with_hidden_password, indent=4)),
    )

    response = send_aviatrix_api(
        api_endpoint_url=api_endpoint_url,
        request_method=request_method,
        payload=data_2nd_try,
    )

    return response


# End def set_admin_password()


def verify_aviatrix_api_set_admin_password(response=None):
    # if the set admin password request is successful
    # the response code is 200 and the return true
    py_dict = response.json()
    logging.info("Aviatrix API response is %s", str(py_dict))

    response_code = response.status_code
    if response_code != 200:
        err_msg = (
                "Fail to set admin password, the response code is : "
                + str(response_code)
                + ", which is not 200"
        )
        raise AviatrixException(message=err_msg)

    api_return_boolean = py_dict["return"]
    if api_return_boolean is not True:
        err_msg = (
                "Fail to set admin password for Aviatrix Controller. API response is :"
                + str(py_dict)
        )
        raise AviatrixException(message=err_msg)


# End def verify_aviatrix_api_set_admin_password()


def run_initial_setup(
        api_endpoint_url="123.123.123.123/v1/api",
        CID="ABCD1234",
        target_version="latest",
):
    request_method = "POST"

    # Step1 : Check if the controller has been already initialized
    #       --> yes
    #       --> no --> run init setup (upgrading to the latest controller version)
    data = {"action": "initial_setup", "CID": CID, "subaction": "check"}
    logging.info("Check if the initial setup has been already done or not")
    response = send_aviatrix_api(
        api_endpoint_url=api_endpoint_url,
        request_method=request_method,
        payload=data,
    )
    py_dict = response.json()
    # The initial setup has been done
    if py_dict["return"] is True:
        logging.info("Initial setup for Aviatrix Controller has been already done")
        return response

    # The initial setup has not been done yet
    data = {
        "action": "initial_setup",
        "CID": CID,
        "target_version": target_version,
        "subaction": "run",
    }

    logging.info("API endpoint url: %s", str(api_endpoint_url))
    logging.info("Request method is: %s", str(request_method))
    logging.info("Request payload is : %s", str(json.dumps(obj=data, indent=4)))
    try:
        # response = send_aviatrix_api(
        #     api_endpoint_url=api_endpoint_url,
        #     request_method=request_method,
        #     payload=data,
        #     retry_count=1,
        #     timeout=300,
        # )
        response = requests.post(url=api_endpoint_url, data=data, verify=False, timeout=600)
    except requests.exceptions.Timeout as e:
        logging.exception("WARNING: Request timeout...")
        return None
    # except AviatrixException as ae:
    #     # Ignore timeout exception since it is expected
    #     if "Read timed out" in str(ae):
    #         return None
    except:
        raise
    return response


# End def run_initial_setup()


def verify_aviatrix_api_run_initial_setup(response=None):
    if not response:
        return
    py_dict = response.json()
    logging.info("Aviatrix API response is: %s", str(py_dict))

    response_code = response.status_code
    if response_code != 200:
        err_msg = (
                "Fail to run initial setup for the Aviatrix Controller. The actual response code is "
                + str(response_code)
                + ", which is not 200"
        )
        raise AviatrixException(message=err_msg)

    api_return_boolean = py_dict["return"]
    if api_return_boolean is not True:
        err_msg = (
                "Fail to run initial setup for the Aviatrix Controller. The actual api response is  "
                + str(py_dict)
        )
        raise AviatrixException(message=err_msg)
    pass


# End def verify_aviatrix_api_run_initial_setup()


def set_aviatrix_customer_id(
        api_endpoint_url="https://123.123.123.123/v1/api",
        CID="ABCD1234",
        customer_id="aviatrix-1234567.89",
):
    request_method = "POST"
    data = {"action": "setup_customer_id", "CID": CID, "customer_id": customer_id}

    logging.info("API endpoint url: %s", str(api_endpoint_url))
    logging.info("Request method is: %s", str(request_method))
    logging.info("Request payload is : %s", str(json.dumps(obj=data, indent=4)))

    response = send_aviatrix_api(
        api_endpoint_url=api_endpoint_url,
        request_method=request_method,
        payload=data,
    )
    return response


# End def set_aviatrix_customer_id()


def create_access_account(
        api_endpoint_url="https://123.123.123.123/v1/api",
        CID="ABCD1234",
        account_name="my-aws-role-based",
        account_password="**********",
        account_email="test@aviatrix.com",
        cloud_type="1",
        aws_account_number="123456789012",
        is_iam_role_based="true",
        app_role_arn="arn:aws:iam::123456789012:role/aviatrix-role-app",
        ec2_role_arn="arn:aws:iam::123456789012:role/aviatrix-role-ec2",
):
    request_method = "POST"
    if cloud_type == "1":
        data = {
            "action": "setup_account_profile",
            "CID": CID,
            "account_name": account_name,
            "account_password": account_password,
            "account_email": account_email,
            "cloud_type": cloud_type,
            "aws_account_number": aws_account_number,
            "aws_iam": is_iam_role_based,
            "aws_role_arn": app_role_arn,
            "aws_role_ec2": ec2_role_arn
        }
    elif cloud_type == "1024":
        data = {
            "action": "setup_account_profile",
            "CID": CID,
            "account_name": account_name,
            "account_password": account_password,
            "account_email": account_email,
            "cloud_type": cloud_type,
            "aws_china_account_number": aws_account_number,
            "aws_china_iam": is_iam_role_based,
            "aws_china_role_arn": app_role_arn,
            "aws_china_role_ec2": ec2_role_arn
        }

    payload_with_hidden_password = dict(data)
    payload_with_hidden_password["account_password"] = "************"

    logging.info("API endpoint url: %s", str(api_endpoint_url))
    logging.info("Request method is: %s", str(request_method))
    logging.info(
        "Request payload is : %s",
        str(json.dumps(obj=payload_with_hidden_password, indent=4)),
    )

    response = send_aviatrix_api(
        api_endpoint_url=api_endpoint_url,
        request_method=request_method,
        payload=data,
    )

    return response


# End def create_access_account()

def verify_aviatrix_api_create_access_account(
        response=None,
        admin_email="test@aviatrix.com",
):
    py_dict = response.json()
    logging.info("Aviatrix API response is: %s", str(py_dict))

    response_code = response.status_code
    if response_code != 200:
        err_msg = (
                "Fail to create the access account. The actual response code is : "
                + str(response_code)
                + ", which is not 200"
        )
        raise AviatrixException(message=err_msg)
    api_return_boolean = py_dict["return"]
    if api_return_boolean is not True:
        if "already exists" in py_dict["reason"]:
            return
        err_msg = "Fail to create the access account. The response is : " + str(py_dict)
        raise AviatrixException(message=err_msg)

    api_return_msg = py_dict["results"]
    expected_string = "An email confirmation has been sent to {email_address}"
    expected_string = expected_string.format(email_address=admin_email)
    if (expected_string in api_return_msg) is False:
        avx_err_msg = (
                "Fail to create the access account. API actual return message is: "
                + str(py_dict)
                + " The string we expect to find is: "
                + expected_string
        )
        raise AviatrixException(
            message=avx_err_msg,
        )


# End def verify_aviatrix_api_create_access_account()

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s aviatrix-aws-function--- %(message)s", level=logging.INFO
    )

    controller_launch_wait_time = sys.argv[1]
    aws_account_id = sys.argv[2]
    public_ip = sys.argv[3]
    private_ip = sys.argv[4]
    admin_email = sys.argv[5]
    new_admin_password = sys.argv[6]
    account_email = sys.argv[7]
    controller_version = sys.argv[8]
    access_account_name = sys.argv[9]
    customer_license_id = sys.argv[10]
    ec2_role_name = sys.argv[11]
    app_role_name = sys.argv[12]
    controller_region = sys.argv[13]

    event = {
        "controller_launch_wait_time": int(controller_launch_wait_time),
        "aws_account_id": aws_account_id,
        "public_ip": public_ip,
        "private_ip": private_ip,
        "aviatrix_api_version": "v1",
        "aviatrix_api_route": "api",
        "admin_email": admin_email,
        "new_admin_password": new_admin_password,
        "controller_init_version": controller_version,
        "account_email": account_email,
        "customer_license_id": customer_license_id,
        "access_account_name": access_account_name,
        "ec2_role_name": ec2_role_name,
        "app_role_name": app_role_name,
        "controller_region": controller_region,
    }

    try:
        function_handler(event)
    except Exception as e:
        logging.exception("")
    else:
        logging.info(
            "Aviatrix Controller %s has been initialized successfully", public_ip
        )

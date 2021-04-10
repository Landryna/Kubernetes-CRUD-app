from radish import given, when, then, world, step
from retry import retry
import subprocess
import os
import requests


@retry(AssertionError, tries=10, delay=2)
def wait_for_proper_proc_exist_status(proc):
    """
    Wait for proper process exit status code
    :param proc: Process
    """
    assert proc.poll() != 0, "Application process is still running"


@retry(requests.ConnectionError, tries=10, delay=2)
def wait_for_port_connectivity(url):
    """
    Wait for port connectivity
    :param url: URL
    :return: Response
    """
    return requests.get(url)


@given('flask application tries to start on port {port:QuotedString}')
def try_to_start_app(step, port):
    # Set FLASK_APP env variable and starting process which runs the app.
    world.config.user_data["host"] = "localhost"
    world.config.user_data["port"] = port
    os.environ['FLASK_APP'] = '../src/main.py'
    world.config.user_data['process'] = \
        subprocess.Popen(
            ["flask", "run", "--port", port],
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)


@when('GET request is sent to {host:QuotedString}')
def send_get_request(step, host):
    step.context.response = wait_for_port_connectivity(f"http://{host}")


@then('status code is {status_code:QuotedString}')
def check_status_code(step, status_code):
    assert step.context.response.status_code == int(status_code), \
        f"Actual status code: '{step.context.response.status_code}'.\n Expected status code: '{int(status_code)}'"


@when('flask application finishes with non-zero exit status')
def check_exit_status(step):
    wait_for_proper_proc_exist_status(world.config.user_data['process'])


@then('{error_message:QuotedString} is logged')
def check_logged_msg(step, error_message):
    output = world.config.user_data['process'].stderr.read().decode("utf-8")
    assert error_message in output, f"Expected error msg: {error_message} not in output: f{output}"

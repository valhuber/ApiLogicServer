import requests
import json
from dotmap import DotMap

def prt(msg: any, test: str= None) -> None:
    """
    print to console, and logic_logger / server_log (see api/customize_api.py)

    @see api/customize_api/py for implementation.

    :param msg: message to be written to logs.  Value "Rules Report" writes rules report to logs
    :param test: name of test (scenario) - directs output to test/logs
    :return:
    """
    test_val = test
    if test is not None and len(test) >= 26:
        test_val = test[0:25]
    msg_url = f'http://localhost:5656/server_log?msg={msg}&test={test}&dir=test/api_logic_server_behave/logs/scenario_logic_logs'
    r = requests.get(msg_url)

def login():
    post_uri = 'http://localhost:5656/api/auth/login'
    post_data = {"username": "aneu", "password": "p"}
    r = requests.post(url=post_uri, json = post_data)
    response_text = r.text
    status_code = r.status_code
    if status_code > 300:
        raise Exception(f'POST login failed with {r.text}')
    result_data = json.loads(response_text)
    result_map = DotMap(result_data)
    token = result_map.access_token

    # https://stackoverflow.com/questions/19069701/python-requests-library-how-to-pass-authorization-header-with-single-token
    header = {'Authorization': 'Bearer {}'.format(f'{token}')}
    save_for_session = True
    if save_for_session:
        s = requests.Session()
        s.headers.update(header)
    return header


if __name__ == "__main__":
    print(f'\n test_services.py, starting')

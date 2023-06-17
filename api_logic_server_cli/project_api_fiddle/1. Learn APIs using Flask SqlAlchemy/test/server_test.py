import sys
from pathlib import Path
import requests
import logging
import json
import json


def server_tests(host, port, version):
    """ 
        args
            host - server host
            port - server port
            version - ApiLogicServer version
    """

    print(f'\n\n\nVerify ALFKI returned...\n')
    get_order_uri = f'http://localhost:8080/order?Id=10643'
    r = requests.get(url=get_order_uri)
    response_text = r.text

    assert "ALFKI" in response_text, f'Error - "ALFKI not in {response_text}'

    dictData= json.loads(response_text)
    print(dictData)
    assert dictData["CustomerId"] == "ALFKI", f'Error - "dictData["CustomerId"] is not ALFKI'

    print(f'\nTEST PASSED\n')
    

if __name__ == "__main__":
    server_tests("localhost", "8080", "v0")

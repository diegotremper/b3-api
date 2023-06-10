import os

import requests


def open_test_file(request, name):
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)
    with open("{}/{}".format(test_dir, name)) as f:
        return f.read()


def patch_request_session(mocker):
    mocker.patch(
        "b3_api.api_utils.request_session", return_value=requests.Session()
    )

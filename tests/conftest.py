from pathlib import Path

import pytest


@pytest.fixture
def get_request() -> str:
    path = Path("data/get.txt")
    with open(path, "r") as f:
        data = f.read()

    return data


@pytest.fixture
def html_resp() -> str:
    path = Path("data/html_resp.txt")
    with open(path, "r") as f:
        data = f.read()

    return data


@pytest.fixture
def malformed_request() -> str:
    path = Path("data/malformed.txt")
    with open(path, "r") as f:
        data = f.read()

    return data


@pytest.fixture
def post_form_request() -> str:
    path = Path("data/post_form.txt")
    with open(path, "r") as f:
        data = f.read()

    return data


@pytest.fixture
def post_json_request() -> str:
    path = Path("data/post_json.txt")
    with open(path, "r") as f:
        data = f.read()

    return data

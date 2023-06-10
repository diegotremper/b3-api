import pytest

import tests.utils as utils
from b3_api.historical_series_download import historical_series_download


def test_annual_data(mocker, requests_mock):
    utils.patch_request_session(mocker)
    requests_mock.get(
        "https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A2010.ZIP",
        text="test_annual_data",
    )
    content = historical_series_download(year=2010)
    assert content.decode("utf-8") == "test_annual_data"


def test_monthly_data(mocker, requests_mock):
    utils.patch_request_session(mocker)
    requests_mock.get(
        "https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_M012023.ZIP",
        text="test_monthly_data",
    )
    content = historical_series_download(year=2023, month=1)
    assert content.decode("utf-8") == "test_monthly_data"


def test_daily_data(mocker, requests_mock):
    utils.patch_request_session(mocker)
    requests_mock.get(
        "https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_D02012010.ZIP",
        text="test_daily_data",
    )
    content = historical_series_download(year=2010, month=1, day=2)
    assert content.decode("utf-8") == "test_daily_data"


def test_404(mocker, requests_mock):
    utils.patch_request_session(mocker)
    requests_mock.get(
        "https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_D01012010.ZIP",
        text="not_found",
        status_code=404,
    )
    with pytest.raises(Exception) as excinfo:
        historical_series_download(year=2010, month=1, day=1)

    assert (
        str(excinfo.value)
        == "Error downloading file COTAHIST_D01012010.ZIP, code: 404"
    )
